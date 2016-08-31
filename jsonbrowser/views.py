from flask import render_template
from jsonbrowser.content.creation import get_example_content
from jsonbrowser.es import create_es_mapping
from jsonbrowser.es import delete_index
from jsonbrowser.es import get_doc
from jsonbrowser.es import index_item
from jsonbrowser.es import query_by_path
from jsonbrowser.es import query_by_type
from jsonbrowser.flask_app import app
import os


FULL_TITLE_ATTRS = {
    'opengever.repository.repositoryfolder': '_title_with_refnum',
}


def tree_from_nodes(nodes, sortkey=None):
    """Creates a nested tree of nodes from a flat list-like object of nodes.
    Each node is expected to be a dict with a path-like string stored
    under the key ``_path``.
    Each node will end up with a ``nodes`` key, containing a list
    of children nodes.
    The nodes are changed in place, be sure to make copies first when
    necessary.

    If given, orders nodes by `sortkey`.
    """
    if sortkey is not None:
        nodes.sort(key=lambda node: node.get(sortkey))

    for node in nodes:
        node['nodes'] = []

    nodes_by_path = dict((node['_path'], node) for node in nodes)
    root = []

    for node in nodes:
        parent_path = os.path.dirname(node['_path'])
        if parent_path in nodes_by_path:
            nodes_by_path[parent_path]['nodes'].append(node)
        else:
            root.append(node)

    return root


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/theme-test')
def theme_test():
    return render_template('theme-test.html')


@app.route('/repofolders/')
def list_repofolders():
    _type = 'opengever.repository.repositoryfolder'
    repofolders = query_by_type(_type)

    full_title_attr = FULL_TITLE_ATTRS.get(_type, 'title')
    nodes = [
        {'_id': n['_id'],
         '_path': n['_source']['_path'],
         '_full_title': n['_source'].get(full_title_attr),
         '_sortable_refnum': n['_source']['_sortable_refnum'],
         }
        for n in repofolders]
    tree = tree_from_nodes(nodes, sortkey='_sortable_refnum')

    return render_template('repofolders.html', repofolders=tree)


@app.route('/view/<_type>/<es_id>')
def view_item(_type, es_id):
    doc = get_doc(_type, es_id)
    return render_template('view_item.html', doc=doc)


@app.route('/browse/<path:obj_path>')
def browse(obj_path):
    obj_path = '/%s' % obj_path.strip('/')
    doc = query_by_path(obj_path)

    return render_template('browse.html', doc=doc)


@app.route('/reindex')
def reindex():
    delete_index()
    create_es_mapping()
    data = get_example_content()
    for item in data:
        index_item(item)

    return str({'status': 'success'})
