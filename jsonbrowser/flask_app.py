from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap
from jsonbrowser.content.creation import create_example_content
from jsonbrowser.db import db
from jsonbrowser.models.todo import Todo


def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    return app


app = create_app()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../dev.db'

db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/theme-test')
def theme_test():
    return render_template('theme-test.html')


@app.route('/todos/')
def list_todos():
    todos = Todo.query.all()
    return render_template('todos.html', todos=todos)


@app.route('/todos/<todo_id>')
def view_todo(todo_id):
    todo = Todo.query.filter_by(id=todo_id).one()
    return render_template('todo.html', todo=todo)


def initdb():
    """Init/reset database."""
    db.drop_all()
    db.create_all()
    create_example_content(db)


def run_server():
    app.test_request_context().push()
    initdb()
    app.run(debug=True)


if __name__ == '__main__':
    run_server()
