"""
Transform a JSON file with content dumped via plone.restapi into
a format usable by ftw.inflator.
"""

from urlparse import urlparse
import json
import sys

SITE_ABBR = 'FD'
REFNUM_DELIMITER = '.'


def url_to_path(item):
    value = item['@id']
    parsed_url = urlparse(value)
    item['_path'] = parsed_url.path.rstrip('/')
    item.pop('@id')
    return item


def refnum_to_sortable_refnum(item):
    parts = map(int, item['_refnum'].split('.'))
    padded = ['%03d' % n for n in parts]
    _sortable_refnum = '-'.join(padded)
    item['_sortable_refnum'] = _sortable_refnum
    return item


def extract_refnum(item):
    refnum = item['_meta_reference']
    if refnum is not None:
        assert refnum.startswith(SITE_ABBR)
        refnum = refnum.replace(SITE_ABBR, '').strip()
        item['_refnum'] = refnum

        # Deal with templates and other objs with fake refnums
        if item['_refnum'].startswith('/ '):
            item['_refnum'] = item['_refnum'].replace('/ ', '', 1)

        item.pop('_meta_reference')
    return item


def build_title_with_refnum(item):
    title = item['title']
    title_with_refnum = '%s %s' % (item['_refnum'], title)
    item['_title_with_refnum'] = title_with_refnum
    return item


def translated_title_to_title(item):
    if 'title_de' in item:
        title_de = item['title_de']
        item['title'] = title_de
        item.pop('title_de')
        item.pop('title_fr')
    return item


KEYS_TO_DROP = [
    u'UID',
    u'parent',
    u'items',
]

KEYS_TO_RENAME = {
    u'@type': u'_type',
}

TRANSFORMS = [
    url_to_path,
    translated_title_to_title,
    extract_refnum,
    refnum_to_sortable_refnum,
    build_title_with_refnum,
]


def rename_key(item, old_key, new_key):
    if old_key in item:
        assert new_key not in item
        item[new_key] = item.pop(old_key)
    return item


def transform_item(item):
    for old_key, new_key in KEYS_TO_RENAME.items():
        rename_key(item, old_key, new_key)

    for key in KEYS_TO_DROP:
        item.pop(key, None)

    for transform in TRANSFORMS:
        item = transform(item)

    # Drop all unprocessed metadata
    for key in item.keys():
        if key.startswith('_meta_'):
            item.pop(key)

    return item


def dump_pretty_json(data, stream):
    json.dump(
        data, stream,
        sort_keys=True,
        indent=4,
        separators=(',', ': '))


def main(in_path, out_path):
    with open(in_path) as json_file:
        data = json.load(json_file)

    new_items = []
    for item in data:
        item = transform_item(item)
        new_items.append(item)

    with open(out_path, 'w') as out_file:
        dump_pretty_json(new_items, out_file)


if __name__ == '__main__':
    in_path = sys.argv[1]
    out_path = sys.argv[2]
    main(in_path, out_path)
