"""WSGI application."""
import os
from sys import argv
from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware

from tweetTrack.app import app

application = DispatcherMiddleware(app)

if __name__ == '__main__':

    if len(argv) < 2:
        os.environ['FLASK_CONFIG'] = 'Dev'
    else:
        os.environ['FLASK_CONFIG'] = argv[1].title()

    run_simple(
        'localhost',
        8000,
        application
    )
