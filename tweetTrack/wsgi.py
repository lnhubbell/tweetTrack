"""WSGI application."""
import os
from sys import argv
from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware

from tweetTrack.app import app

application = DispatcherMiddleware(app)

if __name__ == '__main__':
    if len(argv) < 2 or argv[1] == 'Dev':
        os.environ['FLASK_CONFIG'] = 'Dev'
        run_simple(
            'localhost',
            5000,
            application,
            __debug__
        )
    else:
        os.environ['FLASK_CONFIG'] = argv[1].title()
        print(os.environ['FLASK_CONFIG'])
        run_simple(
            'localhost',
            5000,
            application,
        )
