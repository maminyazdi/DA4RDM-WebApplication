from flask import (
    Blueprint, render_template, request
)

import da4rdm.api.api as api
preprocessing_bp = Blueprint('blueprints/preprocessing', __name__, template_folder='templates', static_folder='static')

@preprocessing_bp.route('/')
def preprocessing():
    data_sources = api.get_all_data_sources()
    pipeline_names = api.get_all_pipeline_names()
    return render_template('preprocessing/preprocessing.html', data_sources=data_sources, pipelines=pipeline_names)

@preprocessing_bp.route('/view_project')
def view_project():
    project_name = request.args['project_name']
    pipeline_parameters = request.args['pipelineParameters']
    return render_template('preprocessing/view_project.html', project_name = project_name, pipeline_parameters = pipeline_parameters)

@preprocessing_bp.route('/data_source_new')
def new_data_source():
    return render_template('preprocessing/data_source_new.html')

@preprocessing_bp.route('/data_source_select')
def data_source_select():
    data_sources = api.get_all_data_sources()
    return render_template('preprocessing/data_source_select.html', data_sources=data_sources)