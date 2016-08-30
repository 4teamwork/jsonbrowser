"""
Utility functions for creating example content
"""

from jsonbrowser.content.exampledata import dev
from jsonbrowser.content.factories import TodoFactory


def create_example_content():
    todos = []
    for item in dev.TODOS:
        todo = TodoFactory(item).create()
        todos.append(todo)

    return todos
