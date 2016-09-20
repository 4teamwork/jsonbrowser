"""
Utility functions for creating example content
"""

from pkg_resources import resource_filename
import json
import os


VAR_DIR = os.path.normpath(resource_filename('jsonbrowser', "../var"))

TYPES = [
    'opengever.repository.repositoryroot',
    'opengever.repository.repositoryfolder',
    'opengever.dossier.businesscasedossier',
    'opengever.document.document',
    'ftw.mail.mail',
    'opengever.task.task',
]


def get_content():
    data = []
    for _type in TYPES:
        json_path = os.path.join(VAR_DIR, '%s.json' % _type)
        with open(json_path) as json_file:
            items = json.load(json_file)
            data.extend(items)
    return data
