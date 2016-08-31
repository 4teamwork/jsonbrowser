class Config(object):
    DEBUG = False
    TESTING = False
    PLONE_SITE_TITLE = 'Plone Site'

    # To be set in jsonbrowser.cfg in instance folder:
    # SESSION_SECRET = '<secret>'


class DevelopmentConfig(Config):
    DEBUG = True
    PLONE_SITE_ID = 'fd'
