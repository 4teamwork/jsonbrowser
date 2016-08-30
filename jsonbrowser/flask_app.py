from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap
from jsonbrowser.content.creation import create_example_content


TODOS = []


def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    return app


app = create_app()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/theme-test')
def theme_test():
    return render_template('theme-test.html')


@app.route('/todos/')
def list_todos():
    todos = TODOS
    return render_template('todos.html', todos=todos)


@app.route('/todos/<int:todo_id>')
def view_todo(todo_id):
    todo = TODOS[todo_id - 1]
    return render_template('todo.html', todo=todo)


def run_server():
    global TODOS
    app.test_request_context().push()
    TODOS = create_example_content()
    app.run(debug=True)


if __name__ == '__main__':
    run_server()
