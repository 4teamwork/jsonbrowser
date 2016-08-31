import json
import requests


AUTH = ('username', 'password')
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


def fetch_items(session, item_urls):
    for url in item_urls:
        print "Fetching: %s" % url
        response = session.get(url)
        item = response.json()
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


def main():
    with requests.Session() as session:
        headers = {'Accept': 'application/json'}
        session.headers.update(headers)
        session.auth = AUTH
        verify_auth(session)
        crawl(session)
        dump_catalog()
        fetch_items_for_all_types(session)


if __name__ == '__main__':
    main()
