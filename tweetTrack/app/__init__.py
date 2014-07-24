import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail
from config import config

app = Flask(__name__)
flask_config = os.environ.get('FLASK_CONFIG', 'Prod')
if flask_config == 'Dev':
    print('starting in Dev mode')
    app.config.from_object(config.DevelopmentConfig)
else:
    print('starting in Prod mode')
    app.config.from_object(config.ProductionConfig)
db = SQLAlchemy(app)
mail = Mail(app)

from tweetTrack.app import views