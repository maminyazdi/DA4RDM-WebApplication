import os
import sqlalchemy
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO, emit

from config import Config

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)
socketio = SocketIO(app, ping_timeout=app.config["PING_TIMEOUT"], ping_interval=app.config["PING_INTERVALL"])

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from . import main
app.register_blueprint(main.bp)
app.add_url_rule('/', endpoint='index')

from . import preprocessing
app.register_blueprint(preprocessing.preprocessing_bp, url_prefix="/preprocessing")

from . import processMining
app.register_blueprint(processMining.process_mining_bp, url_prefix="/process_mining")

from .api import api
app.register_blueprint(api.api_bp, url_prefix='/api')

socketio.run(app) # if using socketio I cannot make use of the app factory, so app will stay in the global name space. I need to make sure that the unit testing will be working correctly anyway

from da4ds import models
