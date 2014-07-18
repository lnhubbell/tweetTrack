from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import config


app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
db = SQLAlchemy(app)

from tweetTrack.app import views