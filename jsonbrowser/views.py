from flask import render_template
from jsonbrowser.content.creation import get_example_content
from jsonbrowser.flask_app import app
from requests.exceptions import ConnectionError
import os
import requests


ES_BASE = 'http://localhost:9200/'
ES_INDEX = 'migration'
ES_URL = ''.join((ES_BASE, ES_INDEX))
ES_MAX_PAGE_SIZE = 9999


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
    url = '%s/%s/_search?size=%s' % (ES_URL, _type, ES_MAX_PAGE_SIZE)
    query = {'sort': ['_sortable_refnum']}
    response = requests.get(url, json=query)
    resultset = response.json()
    assert resultset['hits']['total'] <= ES_MAX_PAGE_SIZE
    repofolders = resultset['hits']['hits']

    nodes = [
        {'_id': n['_id'],
         '_path': n['_source']['_path'],
         'title': n['_source']['title'],
         '_sortable_refnum': n['_source']['_sortable_refnum'],
         }
        for n in repofolders]
    tree = tree_from_nodes(nodes, sortkey='_sortable_refnum')

    return render_template('repofolders.html', repofolders=tree)


@app.route('/view/<_type>/<es_id>')
def view_item(_type, es_id):
    url = '%s/%s/%s' % (ES_URL, _type, es_id)
    response = requests.get(url)
    doc = response.json()
    return render_template('view_item.html', doc=doc)


@app.route('/reindex')
def reindex():
    data = get_example_content()
    for _id, item in enumerate(data):
        _type = item.pop('_type')
        url = '/'.join((ES_URL, _type, str(_id)))
        try:
            response = requests.put(url, json=item)
        except ConnectionError:
            msg = ("Couldn't connect to ElasticSearch at %s - please "
                   "make sure ES is running." % ES_URL)
            print msg
            raise

        if response.status_code not in (200, 201):
            raise Exception((response.status_code, response.text))

    return str({'status': 'success'})
