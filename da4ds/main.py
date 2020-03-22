import os
import re
import csv
import sqlalchemy
import importlib
from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, jsonify, current_app as app
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from da4ds import db
import da4ds.api.api as api
bp = Blueprint('blueprints/main', __name__)

@bp.route('/')
def index():
    projects_path = app.config['USER_PROJECT_DIRECTORY']
    if projects_path[-1] != '/':
        projects_path += '/'
    dirs = os.listdir(projects_path)
    projects_directories = [str(x) for x in dirs if (os.path.isdir(projects_path + x) and x != '__pycache__')]

    return render_template('main/index.html', projects = projects_directories)
