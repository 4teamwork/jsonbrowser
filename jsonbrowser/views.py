from flask import render_template
from jsonbrowser.content.creation import get_example_content
from jsonbrowser.flask_app import app
from requests.exceptions import ConnectionError
import requests


ES_BASE = 'http://localhost:9200/'
ES_INDEX = 'migration'
ES_URL = ''.join((ES_BASE, ES_INDEX))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/theme-test')
def theme_test():
    return render_template('theme-test.html')


@app.route('/repofolders/')
def list_repofolders():
    _type = 'opengever.repository.repositoryroot'
    url = '%s/%s/_search' % (ES_URL, _type)
    response = requests.get(url)
    repofolders = response.json()['hits']['hits']
    return render_template('repofolders.html', repofolders=repofolders)


@app.route('/repofolders/<repofolder_id>')
def view_repofolder(repofolder_id):
    _type = 'opengever.repository.repositoryroot'
    url = '%s/%s/%s' % (ES_URL, _type, repofolder_id)
    response = requests.get(url)
    repofolder = response.json()
    return render_template('repofolder.html', repofolder=repofolder)


@app.route('/reindex')
def reindex():
    data = get_example_content()
    for _id, item in enumerate(data):
        _type = item.pop('_type')
        url = '/'.join((ES_URL, _type, str(_id)))
        try:
            response = requests.put(url, json=item)
        except ConnectionError:
            msg = ("Couldn't connect to ElasticSearch at %s - please "
                   "make sure ES is running." % ES_URL)
            print msg
            raise

        if response.status_code not in (200, 201):
            raise Exception((response.status_code, response.text))

    return str({'status': 'success'})
