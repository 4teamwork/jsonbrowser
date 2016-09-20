"""
Utility functions for loading JSON datasets
"""

from jsonbrowser.flask_app import app
from jsonbrowser.utils import mkdir_p
import json
import os


DATASET_DIR = os.path.join(app.instance_path, 'dataset')

TYPES = [
    'opengever.repository.repositoryroot',
    'opengever.repository.repositoryfolder',
    'opengever.dossier.businesscasedossier',
    'opengever.document.document',
    'ftw.mail.mail',
    'opengever.task.task',
]


def get_content():
    mkdir_p(DATASET_DIR)
    data = []
    for _type in TYPES:
        json_path = os.path.join(DATASET_DIR, '%s.json' % _type)
        with open(json_path) as json_file:
            items = json.load(json_file)
            data.extend(items)
    return data
