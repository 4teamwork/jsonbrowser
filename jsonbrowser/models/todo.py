"""
Todo model
"""

from jsonbrowser.db import db


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)

    def __repr__(self):
        rep = u"<Todo %r>" % self.name
        return rep.encode('utf-8')
