from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail
from config import config


app = Flask(__name__)
app.config.from_object(config.ProductionConfig)
db = SQLAlchemy(app)
mail = Mail(app)

from tweetTrack.app import views