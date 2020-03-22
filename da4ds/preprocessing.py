import sqlalchemy
from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, jsonify, current_app as app
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from da4ds import db
import da4ds.api.api as api
preprocessing_bp = Blueprint('blueprints/preprocessing', __name__, template_folder='templates', static_folder='static')

@preprocessing_bp.route('/')
def preprocessing():
    data_sources = api.get_all_data_sources()
    pipeline_names = api.get_all_pipeline_names()
    return render_template('preprocessing/preprocessing.html', data_sources=data_sources, pipelines=pipeline_names)

@preprocessing_bp.route('/view_project')
def view_project():
    project_name = request.args['project_name']
    return render_template('preprocessing/view_project.html', project_name = project_name)

@preprocessing_bp.route('/data_source_new')
def new_data_source():
    return render_template('preprocessing/data_source_new.html')

@preprocessing_bp.route('/data_source_select')
def data_source_select():
    data_sources = api.get_all_data_sources()
    return render_template('preprocessing/data_source_select.html', data_sources=data_sources)