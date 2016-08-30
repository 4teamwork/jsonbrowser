"""
Utility functions for creating example content
"""

from jsonbrowser.content.exampledata import dev
from jsonbrowser.content.factories import TodoFactory


def create_example_content(db):
    db.create_all()

    for item in dev.TODOS:
        todo = TodoFactory(item).create()
        db.session.add(todo)

    db.session.commit()
