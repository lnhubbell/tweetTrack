from os import urandom


class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tweets.db'
    SECRET_KEY = str(urandom(32))


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = """postgres://tweetstalkers:9BBewrkivHctaesd12N7@tweetstalk.cvf1ij0yeyiq.us-west-2.rds.amazonaws.com:5432/lil_tweetstalker"""


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True