import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from config import config

app = Flask(__name__)
flask_config = os.environ.get('FLASK_CONFIG', 'Dev')
if flask_config == 'Dev':
    app.config.from_object(config.DevelopmentConfig)
elif flask_config == 'Prod':
    app.config.from_object(config.ProductionConfig)
db = SQLAlchemy(app)

import views