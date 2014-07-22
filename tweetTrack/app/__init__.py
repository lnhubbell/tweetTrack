from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail


app = Flask(__name__)
try:
    from config import config
    app.config.from_object(config.DevelopmentConfig)
except ImportError:
    pass
app.config.from_object(config.ProductionConfig)
db = SQLAlchemy(app)
mail = Mail(app)

from tweetTrack.app import views