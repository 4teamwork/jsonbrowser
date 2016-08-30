from jsonbrowser import views   # noqa
from jsonbrowser.content.creation import create_example_content
from jsonbrowser.flask_app import app


def run_server():
    app.test_request_context().push()
    create_example_content()
    app.run(debug=True)


if __name__ == '__main__':
    run_server()
