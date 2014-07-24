"""WSGI application."""
import os
from sys import argv
from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware

from streamScript.webAPI import app

application = DispatcherMiddleware(app)

if __name__ == '__main__':
    if len(argv) < 2 or argv[1] == 'Dev':
        os.environ['FLASK_CONFIG'] = 'Dev'
        run_simple(
            'localhost',
            8000,
            application,
            __debug__
        )
    else:
        os.environ['FLASK_CONFIG'] = argv[1].title()
        run_simple(
            'localhost',
            8000,
            application,
        )
