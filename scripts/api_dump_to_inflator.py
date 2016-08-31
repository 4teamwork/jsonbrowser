"""
Transform a JSON file with content dumped via plone.restapi into
a format usable by ftw.inflator.
"""

from urlparse import urlparse
import json
import os
import sys


def url_to_path(item):
    value = item['@id']
    parsed_url = urlparse(value)
    item['_path'] = parsed_url.path.rstrip('/')
    item.pop('@id')
    return item


def path_to_sortable_refnum(item):
    path = item['_path']
    parent_path = os.path.dirname(path)
    _sortable_refnum = '%s-%s' % (parent_path, item['reference_number_prefix'])
    item['_sortable_refnum'] = _sortable_refnum
    return item


def translated_title_to_title(item):
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
    path_to_sortable_refnum,
    translated_title_to_title,
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
