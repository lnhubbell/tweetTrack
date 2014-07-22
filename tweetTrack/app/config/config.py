from os import urandom, environ


class Config(object):
    DEBUG = environ.get('DEBUG', False)
    TESTING = environ.get('TESTING', False)
    SQLALCHEMY_DATABASE_URI = environ.get(
        'SQLALCHEMY_DATABASE_URI',
        "sqlite:///tweets.db"
    )
    SECRET_KEY = environ.get('SECRET_KEY', str(urandom(32)))
    CSRF_ENABLED = environ.get('CSRF_ENABLED', True)
    MAIL_SERVER = environ.get('MAIL_SERVER', "smtp.gmail.com")
    MAIL_PORT = environ.get('MAIL_PORT', 465)
    MAIL_USE_SSL = environ.get('MAIL_USE_SSL', True)
    MAIL_USERNAME = environ.get('MAIL_USERNAME', 'tweet.track@gmail.com')
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD', 'DoMoreFaster')
    CONSUMER_KEY = environ.get('CONSUMER_KEY', 'hWMHWIJYoJ4UIG0KNwXcC4pbg')
    CONSUMER_SECRET = environ.get(
        'CONSUMER_SECRET',
        '85E7dAk4ZkJEyNkQ0EbxYvavL7FeKUwEEJlXOs9QnXDwIcWL5c'
    )
    ACCESS_KEY = environ.get(
        'ACCESS_KEY',
        '249913463-xJhkkoiipEVF0xIJeZc9dys8N1qovmZGmgqiSLaV'
    )
    ACCESS_SECRET = environ.get(
        'ACCESS_SECRET',
        'q4CleTUfctg4BfQz6R5cRpa8EekBylIRzr63fCuargyDa'
    )


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = environ.get(
        'SQLALCHEMY_DATABASE_URI',
        'postgres://tweetstalkers:9BBewrkivHctaesd12N7@tweetstalk.cvf1ij0yeyiq.us-west-2.rds.amazonaws.com:5432/lil_tweetstalker'
    )


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True