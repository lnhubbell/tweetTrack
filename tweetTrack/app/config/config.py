from os import urandom


class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tweets.sqlite'
    SECRET_KEY = str(urandom(32))


class ProductionConfig(Config):
    DATABASE_URI = 'postgres://user@localhost/foo'


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True