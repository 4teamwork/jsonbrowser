from flask import Flask
from flask_bootstrap import Bootstrap


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    Bootstrap(app)
    return app


app = create_app()
app.config.from_object('jsonbrowser.config.DevelopmentConfig')
app.config.from_pyfile('jsonbrowser.cfg', silent=False)
app.secret_key = app.config['SESSION_SECRET']
