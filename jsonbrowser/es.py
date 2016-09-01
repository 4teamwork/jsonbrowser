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
            },
            "_sortable_refnum": {
                "type": "string",
                "index": "not_analyzed"
            }
        }
    }
    indexdef = {"mappings": {'_default_': default_mapping}}
    response = requests.put(ES_INDEX_URL, json=indexdef)
    return response


def delete_index():
    response = requests.delete(ES_INDEX_URL)
    if response.status_code == 404:
        print "Index %r not found when trying to DELETE" % ES_INDEX
    assert response.status_code in (200, 404)


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


def query_for_children(doc):
    _path = doc['_source']['_path']
    query = {

        "filter": {
            "match": {
                "_parent_path": _path
            }
        },
        "sort": ["_sortable_refnum"],
    }

    url = '%s/_search?size=%s' % (ES_INDEX_URL, ES_MAX_PAGE_SIZE)
    response = requests.get(url, json=query)
    resultset = response.json()
    docs = resultset['hits']['hits']
    return docs


def fulltext_search(search_query):
    url = '%s/_search?size=25&q=%s' % (ES_INDEX_URL, search_query)
    response = requests.get(url)
    resultset = response.json()
    docs = resultset['hits']['hits']
    return docs


def count_objs():
    query = {
        "size": 0,
        "aggs": {
            "type_counts": {
                "terms": {"field": "_type"}
            }
        }
    }
    url = '%s/_search' % ES_INDEX_URL
    response = requests.get(url, json=query)
    resultset = response.json()
    type_counts = resultset['aggregations']['type_counts']['buckets']
    type_counts = dict([(c['key'], c['doc_count']) for c in type_counts])
    return type_counts


def index_item(item):
    print "Indexing item %s" % item['_path']
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


def flush_index():
    url = '%s/_flush' % ES_INDEX_URL
    response = requests.post(url)
    assert response.status_code == 200
