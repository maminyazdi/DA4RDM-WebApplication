import os
import re
import csv
import sqlalchemy
import importlib
import datetime
import pandas as pd
from flask_socketio import emit
from da4ds import socketio

from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, jsonify, current_app as app, send_from_directory, send_file
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from da4ds import db
from da4ds.models import ( InflexibleDataSourceConnection, DataBaseDialect, DialectParameters, DataSource )
from da4ds.processing_libraries.data_source_handler import data_source_handler
from da4ds.process_mining import process_mining_controller, support_functions as process_mining_support
from da4ds.process_mining import event_log_generator
from . import ( user_session, input_parser )

api_bp = Blueprint('blueprints/api', __name__, template_folder='templates', static_folder='static')

"""API methods handle incoming requests and also take care of sesison and authentication related tasks at the highest level."""

@socketio.on('create_new_session', namespace='/api/create_new_session')
def create_new_session():
    session_id = user_session.create_new_session()
    emit('session', session_id) # TODO maybe use simple http request instead of socket or find a way to wait for the response
    return session_id

@api_bp.route('/api/get_all_data_sources')
def get_all_data_sources():
    #TODO veryfy user permissons to access the data sources
    data_sources = db.session.query(DataSource).all()
    return data_sources

@api_bp.route('/new_data_source', methods=['POST'])
def new_data_source():
    # TODO #FIXME IMPORTANT add form validation & escaping
    # generate a new data source entry in the app database
    data_source = DataSource()
    data_source.Name = request.form['dataSourceName']
    data_source.Parameters = request.form['dataSourceParameters']
    data_source.Type = "csv"
    data_source.LastModified = datetime.datetime.now()
    data_source.StoredOnServer = True
    db.session.add(data_source)
    db.session.commit()

    return render_template('preprocessing/preprocessing.html')

@api_bp.route('/read_data_from_source', methods=['POST'])
def read_data_from_source():
    session_id = request.args.get("session_id")
    current_session = user_session.get_session_information(session_id)
    data_sources = get_all_data_sources()
    selected_source = data_sources[int(request.values['selectedDataSourceId']) - 1] # -1 for zero based indexing of data_sources compared to 1 based indexing in db

    dataframe = data_source_handler.read_from_source(selected_source)
    dataframe.to_csv(current_session['data_location'], sep=";") #TODO find a better way to store temporary data i.e. localstorage + uuids TODO make the temporary storage location configurable

    return render_template('preprocessing/preprocessing.html')

@api_bp.route('/get_all_pipeline_names')
def get_all_pipeline_names():
    projects_path = app.config['USER_PROJECT_DIRECTORY']
    if projects_path[-1] != '/':
        projects_path += '/'
    dirs = os.listdir(projects_path)
    projects_directories = [str(x) for x in dirs if (os.path.isdir(projects_path + x) and x != '__pycache__')]
    return projects_directories

@api_bp.route('/run_project', methods=['GET'])
def run_project():
    project_name = request.args['project_name'] # programmatically get the package and module names to import from the given project name
    module_name = "." + project_name
    project_path = app.config['USER_PROJECT_DIRECTORY']
    if project_path[-1] == "/":
        project_path = project_path[0:-1]
    package_name = project_path.replace("/", ".")
    package_name = re.sub(r"^\.*", "", package_name) #replace leading and traling dots
    package_name = re.sub(r"\.*$", "", package_name)

    project = importlib.import_module(module_name, package_name) # import module at runtime
    project_config = project.init(db)
    response = project.run(project_config)

    return response

@socketio.on('requestProjectRun', namespace='/api/run_project')
def run_project_persistent_connection(session_id, data):
    session_information = user_session.get_session_information(session_id)

    # programmatically get the package and module names to import from the given project name
    project_name = data['projectName']
    pipeline_parameters = input_parser.parse_parameter_list(data['pipelineParameters'], ';', '=')
    emit('progressLog', {'message': f"Starting pipeline for project { project_name }"})
    module_name = "." + project_name
    project_path = app.config['USER_PROJECT_DIRECTORY']
    if project_path[-1] == "/":
        project_path = project_path[0:-1]
    package_name = project_path.replace("/", ".")

    #replace leading and traling dots
    package_name = re.sub(r"^\.*", "", package_name)
    package_name = re.sub(r"\.*$", "", package_name)

    # import module at runtime
    project = importlib.import_module(module_name, package_name)
    project_config = project.init(session_information, db, pipeline_parameters)
    response = project.run(project_config)
    emit('json', response)
    return "Pipeline ran successfully."

@socketio.on('requestEventLogPreparation', namespace='/api/run_process_discovery')
def get_process_discovery_filters(session_id, xes_attribute_columns = None, filters = None):
    current_session = user_session.get_session_information(session_id)

    dataframe = pd.read_csv(current_session["data_location"], index_col=0, sep=";")
    column_names = process_mining_support.get_column_names(dataframe)

    if xes_attribute_columns == None and (bool(current_session['pm_xes_attributes']) == False or current_session['pm_xes_attributes'] == None):
        emit("updateColumnNames", column_names)
        return

    if not xes_attribute_columns == None:
        user_session.update_session(session_id, "PMXesAttributes", xes_attribute_columns)

    if not filters == None:
        user_session.update_session(session_id, "PMFilters", filters)

    #process_mining_support.update_xes_attribute_columns(xes_attribute_columns, session_id) # TODO DELETE THOSE FUNCTIONS IN THE HELPER CLASS (UNLESS YOU WANT TO USE THEM TO HANDLE SPECIAL CASES)
    #process_mining_support.update_filters(filters, session_id)

    dataframe = event_log_generator.prepare_event_log_dataframe(dataframe, current_session['pm_xes_attributes'])

    dataframe.to_csv("C:/Temp/aTest.csv", sep=";")

    #get key metrics for the process discovery source data frame
    dataframe_key_metrics = process_mining_controller.get_dataframe_key_metrics(dataframe, current_session['pm_xes_attributes'])

    dataframe.to_csv(current_session["process_mining_data_location"], sep=";")

    emit("ProcessDiscoveryUpdateEverything", {"all_column_names": column_names, # all column names of the data frame
                                              "pm_xes_attributes": current_session['pm_xes_attributes'], # selected xes attribute columns
                                              "pm_filters": current_session['pm_filters'], # selected filters
                                              "pm_dataframe_key_metrics": dataframe_key_metrics}) # key metrics such as number of cases and events #update filters, columns and statistics, other options


    # xes attribute columns + remaining unlabelled columns

    # set filters and filter options

    # create some coherent response object/JSON

    return """Not yet implemented!""" # TODO return to the process mining overview page

### these two functions might be superfluous
@socketio.on('requestProcessMiningFilters', namespace='/api/request_pm_filters')
def get_process_discovery_filters(session_id):
    #TODO filters options need to be updated in accord with previously selected filters.

    current_session = user_session.get_session_information(session_id)
    filter_json = current_session["pm_filters"].to_json()
    emit('json', {"pm_filters": filter_json})

    return """Not yet implemented!""" # TODO return to the process mining overview page

@socketio.on('requestColumnNames', namespace='/api/run_process_discovery')
def get_column_names(session_id):
    current_session = user_session.get_session_information(session_id)
    column_names = process_mining_support.get_column_names(current_session)

    return

@socketio.on('requestColumnNames', namespace='/api/run_process_discovery')
def get_column_names(session_id):
    current_session = user_session.get_session_information(session_id)
    descriptive_stats = process_mining_support.get_descriptive_statistics(current_session)

    emit('json')
    return
###

@socketio.on('requestProcessDiscovery', namespace='/api/run_process_discovery')
def run_process_discovery(session_id):
    emit('progressLog', {"progressLog": "Starting process mining"})
    current_session = user_session.get_session_information(session_id)

    process_model = process_mining_controller.run(current_session)
    emit(process_model[0], process_model[1])

    return

@api_bp.route('/download_temporary_data', methods=['GET'])
def download_temporary_data():
    session_id = request.args["session_id"]
    current_session = user_session.get_session_information(session_id)
    working_data_path = current_session["data_location"].replace('./da4ds/','').replace('/','\\')
    #path_list = working_data_path.split('/')
    #directory_name = '\\\\'.join(path_list[:-1]) + '\\\\'
    #filename = path_list[-1]
    return send_file(working_data_path, as_attachment=True)
    #return send_from_directory(directory_name, filename, as_attachment=True)
    #send_file(working_data_path) #send_from_directory

