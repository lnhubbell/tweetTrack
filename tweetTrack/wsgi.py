"""WSGI application."""

from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware

from tweetTrack.app import app

application = DispatcherMiddleware(app)

if __name__ == '__main__':
    run_simple(
        '0.0.0.0', 5000, application, use_reloader=True, use_debugger=True)
