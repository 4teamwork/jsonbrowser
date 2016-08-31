"""ElasticSearch specific helpers.
"""

from requests.exceptions import ConnectionError
import os
import requests


ES_BASE = 'http://localhost:9200/'
ES_INDEX = 'migration'
ES_INDEX_URL = ''.join((ES_BASE, ES_INDEX))
ES_MAX_PAGE_SIZE = 9999


def create_es_mapping():
    default_mapping = {
        "properties": {
            "_path": {
                "type": "string",
                "index": "not_analyzed"
            },
            "_parent_path": {
                "type": "string",
                "index": "not_analyzed"
            }
        }
    }
    indexdef = {"mappings": {'_default_': default_mapping}}
    response = requests.put(ES_INDEX_URL, json=indexdef)
    return response


def get_doc(_type, es_id):
    url = '%s/%s/%s' % (ES_INDEX_URL, _type, es_id)
    response = requests.get(url)
    doc = response.json()
    return doc


def query_by_type(_type):
    url = '%s/%s/_search?size=%s' % (ES_INDEX_URL, _type, ES_MAX_PAGE_SIZE)
    query = {'sort': ['_sortable_refnum']}
    response = requests.get(url, json=query)
    resultset = response.json()
    assert resultset['hits']['total'] <= ES_MAX_PAGE_SIZE
    docs = resultset['hits']['hits']
    return docs


def query_by_path(obj_path):
    item_query = {
        "filter": {
            "match": {
                "_path": obj_path
            }
        }
    }

    url = '%s/_search' % ES_INDEX_URL
    response = requests.get(url, json=item_query)
    resultset = response.json()
    assert resultset['hits']['total'] == 1
    doc = resultset['hits']['hits'][0]
    return doc


def index_item(item):
    _type = item.pop('_type')
    _parent_path = os.path.dirname(item['_path'])
    item['_parent_path'] = _parent_path
    url = '/'.join((ES_INDEX_URL, _type))
    try:
        response = requests.post(url, json=item)
    except ConnectionError:
        msg = ("Couldn't connect to ElasticSearch at %s - please "
               "make sure ES is running." % ES_INDEX_URL)
        print msg
        raise

    if response.status_code not in (200, 201):
        raise Exception((response.status_code, response.text))
