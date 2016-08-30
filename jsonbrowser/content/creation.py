"""
Utility functions for creating example content
"""

from jsonbrowser.content.exampledata import dev
from jsonbrowser.utils import dump_pretty_json
from jsonbrowser.utils import mkdir_p
from pkg_resources import resource_filename
import json
import os


VAR_DIR = os.path.normpath(resource_filename('jsonbrowser', "../var"))
JSON_PATH = os.path.join(VAR_DIR, 'example.json')


def create_example_content():
    mkdir_p(VAR_DIR)
    with open(JSON_PATH, 'w') as json_file:
        dump_pretty_json(dev.REPOFOLDERS, json_file)
    return JSON_PATH


def get_example_content():
    with open(JSON_PATH) as json_file:
        return json.load(json_file)
