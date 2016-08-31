import json
import requests
import time


AUTH = ('lukas.graf', 'demo10')
SITE_ID = 'fd'
BASE_URL = 'http://localhost:8080/%s' % SITE_ID

TYPES = [
    'opengever.repository.repositoryroot',
    'opengever.repository.repositoryfolder',
    'opengever.dossier.businesscasedossier',
    'opengever.document.document',
    'ftw.mail.mail',
    'opengever.task.task',
]

ADDITIONAL_METADATA = [
    'reference',
]

CATALOG = {}


def query_objs_for_type(session, _type):
    item_urls = []
    query_url = '%s/@search?portal_type=%s' % (BASE_URL, _type)
    next_batch = True
    next_batch_url = query_url
    while next_batch:
        response = session.get(next_batch_url)
        resultset = response.json()

        items = resultset['items']
        for item in items:
            item_urls.append(item['@id'])

        next_batch_url = resultset.get('batching', {}).get('next')
        if next_batch_url is None:
            next_batch = False

    return item_urls


def crawl(session):
    for _type in TYPES:
        item_urls = query_objs_for_type(session, _type)
        CATALOG[_type] = item_urls


def dump_catalog():
    for key in CATALOG:
        print key
        print
        for value in CATALOG[key]:
            print value
        print


def fetch_metadata_for_item(session, item):
        uid = item['UID']
        metadata_query_url = (
            '%s/@search?UID=%s&metadata_fields=_all' % (BASE_URL, uid))
        response = session.get(metadata_query_url)
        assert len(response.json()['items']) == 1
        metadata = response.json()['items'][0]
        return metadata


def fetch_items(session, item_urls):
    for url in item_urls:
        print "Fetching: %s" % url
        response = session.get(url)
        item = response.json()
        if ADDITIONAL_METADATA:
            metadata = fetch_metadata_for_item(session, item)
            for fieldname in ADDITIONAL_METADATA:
                assert fieldname not in item
                meta_key = '_meta_%s' % fieldname
                item[meta_key] = metadata[fieldname]

        yield item


def fetch_items_for_all_types(session):
    for _type in TYPES:
        item_urls = CATALOG[_type]
        type_items = fetch_items(session, item_urls)

        filename = '%s.json' % _type
        with open(filename, 'w') as type_json_file:
            dump_pretty_json(list(type_items), type_json_file)

        print "Dumped items for type %s to %s" % (_type, filename)


def dump_pretty_json(data, stream):
    json.dump(
        data, stream,
        sort_keys=True,
        indent=4,
        separators=(',', ': '))


def verify_auth(session):
    response = session.get(BASE_URL)
    if response.status_code == 401:
        print response.text
        print response.status_code
        raise Exception("Unauthorized")


def count_items(catalog):
    items = 0
    for key in catalog:
        items += len(catalog[key])
    return items


def main():
    start = time.time()

    with requests.Session() as session:
        headers = {'Accept': 'application/json'}
        session.headers.update(headers)
        session.auth = AUTH
        verify_auth(session)
        crawl(session)
        dump_catalog()
        fetch_items_for_all_types(session)

    duration = time.time() - start
    num_items = sum(len(itemlist) for itemlist in CATALOG.itervalues())
    print
    print "Number of items: %s" % num_items
    print "Duration: %.2fs" % duration
    print "Time per item: %.2fs" % (duration / num_items)
    print "Items / s: %.2fs" % (num_items / duration)


if __name__ == '__main__':
    main()
