"""WSGI application."""

from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware

from tweetTrack.app import app

application = DispatcherMiddleware(app)

if __name__ == '__main__':
    run_simple(
        'localhost',
        8000,
        application
    )
