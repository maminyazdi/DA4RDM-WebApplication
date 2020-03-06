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
    print(projects_directories)

    return render_template('main/index.html', projects = projects_directories)

@bp.route('/view_project')
def view_project():
    project_name = request.args['projects']
    return render_template('main/view_project.html', project_name = project_name)

@bp.route('/process_discovery')
def process_discovery():
    return render_template('main/process_discovery.html')

@bp.route('/data_source_new')
def new_data_source():
    return render_template('main/data_source_new.html')

@bp.route('/data_source_select')
def data_source_select():
    data_sources = api.get_all_data_sources()
    return render_template('main/data_source_select.html', data_sources=data_sources)