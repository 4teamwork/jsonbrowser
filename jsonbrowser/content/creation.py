"""
Utility functions for creating example content
"""

from jsonbrowser.content.exampledata import dev
from jsonbrowser.content.factories import RepoFolderFactory


def create_example_content():
    repofolders = []
    for item in dev.REPOFOLDERS:
        repofolder = RepoFolderFactory(item).create()
        repofolders.append(repofolder)

    return repofolders
