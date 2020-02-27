import os
import sqlalchemy
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO, emit

from config import Config

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)
socketio = SocketIO(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from . import main
app.register_blueprint(main.bp)
app.add_url_rule('/', endpoint='index')

from .api import api
app.register_blueprint(api.api_bp, url_prefix='/api')




socketio.run(app) # if using socketio I cannot make use of the app factory, so app will stay in the global name space. I need to make sure that the unit testing will be working correctly anyway


# def create_app(test_config=None):
#     # create and configure the app
#     app = Flask(__name__, instance_relative_config=True)
#     app.config.from_object(Config)

#     db.init_app(app)
#     migrate.init_app(app, db)

#     if test_config is None:
#         # load the instance config, if it exists, when not testing
#         app.config.from_pyfile('config.py', silent=True)
#     else:
#         # Load the test config if passed in
#         app.config.from_mapping(test_config)

#     # Ensure the instance folder exists
#     try:
#         os.makedirs(app.instance_path)
#     except OSError:
#         pass

#     from . import main
#     app.register_blueprint(main.bp)
#     app.add_url_rule('/', endpoint='index')

#     from .api import api
#     app.register_blueprint(api.api_bp, url_prefix='/api')

#     return app

from da4ds import models
