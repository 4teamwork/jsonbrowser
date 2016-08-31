class Config(object):
    DEBUG = False
    TESTING = False

    # To be set in jsonbrowser.cfg in instance folder:
    # SESSION_SECRET = '<secret>'


class DevelopmentConfig(Config):
    DEBUG = True
