from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap
from jsonbrowser.content.creation import create_example_content


REPOFOLDERS = []


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


@app.route('/repofolders/')
def list_repofolders():
    repofolders = REPOFOLDERS
    return render_template('repofolders.html', repofolders=repofolders)


@app.route('/repofolders/<repofolder_id>')
def view_repofolder(repofolder_id):
    repofolder = [r for r in REPOFOLDERS if r.id == repofolder_id][0]
    return render_template('repofolder.html', repofolder=repofolder)


def run_server():
    global REPOFOLDERS
    app.test_request_context().push()
    REPOFOLDERS = create_example_content()
    app.run(debug=True)


if __name__ == '__main__':
    run_server()
