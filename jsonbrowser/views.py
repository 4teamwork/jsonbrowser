from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from jsonbrowser.content.creation import get_content
from jsonbrowser.es import count_objs
from jsonbrowser.es import create_es_mapping
from jsonbrowser.es import delete_index
from jsonbrowser.es import flush_index
from jsonbrowser.es import fulltext_search
from jsonbrowser.es import index_item
from jsonbrowser.es import query_by_path
from jsonbrowser.es import query_by_type
from jsonbrowser.es import query_for_children
from jsonbrowser.flask_app import app
import os
import time


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


def build_navtree():
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
    return tree


@app.route('/')
def index():
    type_counts = count_objs()
    total = sum(type_counts.values())
    return render_template('index.html', type_counts=type_counts, total=total)


@app.route('/theme-test')
def theme_test():
    return render_template('theme-test.html')


@app.route('/browse/')
@app.route('/browse/<path:obj_path>')
def browse(obj_path='/'):
    site_id = app.config['PLONE_SITE_ID']

    if obj_path == '/':
        return redirect(url_for('browse', obj_path=site_id))

    obj_path = '/%s' % obj_path.strip('/')
    if obj_path == '/%s' % site_id:
        # Plone Site Root
        doc = {
            '_type': 'Plone Site',
            '_source': {
                '_path': '/fd',
                '_parent_path': '/',
                'title': app.config['PLONE_SITE_TITLE']
            }
        }
    else:
        doc = query_by_path(obj_path)
    navtree = build_navtree()
    children = query_for_children(doc)
    return render_template(
        'browse.html', doc=doc, navtree=navtree, children=children)


@app.route('/search')
def search():
    query = request.args.get('query')
    docs = fulltext_search(query)
    return render_template('searchresults.html', docs=docs)


@app.route('/reindex')
def reindex():
    start = time.time()

    delete_index()
    create_es_mapping()
    data = get_content()
    for item in data:
        index_item(item)

    duration = time.time() - start
    flush_index()
    flash('Successfully reindexed %s items in %.2fs' % (len(data), duration))
    return redirect(url_for('index'))
