import os
import re
import csv
import sqlalchemy
import datetime
import uuid
import pandas as pd
from flask_socketio import emit
from pm4py.algo.filtering.log.attributes import attributes_filter
from pm4py.algo.filtering.log.variants import variants_filter

from da4rdm import socketio

from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, jsonify, current_app as app, send_from_directory,
    send_file
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from da4rdm import db, Config
from da4rdm.models import (InflexibleDataSourceConnection, DataBaseDialect, DialectParameters, DataSource)
from da4rdm.api.data_source import data_source_handler
from da4rdm.api.process_mining import (process_discovery, event_log_generator, filter_handler,conformance_handler)
from da4rdm.api.preprocessing import user_project_handler
from . import (user_session, input_parser, file_handler)

api_bp = Blueprint('blueprints/api', __name__, template_folder='templates', static_folder='static')

"""API methods handle incoming requests and also take care of sesison and authentication related tasks at the highest level."""


@socketio.on('create_new_session', namespace='/api/create_new_session')
def create_new_session():
    print('New Session Creation')
    session_id = user_session.create_new_session()
    emit('session',
         session_id)  # TODO maybe use simple http request instead of socket or find a way to wait for the response
    return session_id


@api_bp.route('/api/get_all_data_sources')
def get_all_data_sources():
    print('Get all datasources')
    data_sources = db.session.query(DataSource).all()
    return data_sources


@api_bp.route('/new_data_source', methods=['POST'])
def new_data_source():
    print('New datasource')
    session_id = request.args.get("session_id")
    current_session = user_session.get_session_information(session_id)

    name_value = request.form['dataSourceName']
    parameters_value = request.form['dataSourceParameters']
    type_value = request.form['datasource_kind']
    last_modified_value = datetime.datetime.now()

    try:
        data_source_handler.add_datasource(name_value, parameters_value, type_value, last_modified_value, request.files)
    except FileNotFoundError as err:
        flash(err.args[0])
        return redirect(request.url)

    selected_source = db.session.query(DataSource).filter(DataSource.Name == name_value,
                                                          DataSource.Type == type_value,
                                                          DataSource.LastModified == last_modified_value).all()

    dataframe = data_source_handler.read_from_source(selected_source[0])
    dataframe.to_csv(current_session['unmodified_data_location'], sep=";")
    dataframe.to_csv(current_session['data_location'], sep=";")

    data_sources = get_all_data_sources()
    pipeline_names = get_all_pipeline_names()
    return redirect(url_for('blueprints/preprocessing.preprocessing'))

    # return render_template('preprocessing/preprocessing.html', data_sources=data_sources, pipelines=pipeline_names)


# @api_bp.route('/read_data_from_source', methods=['POST'])
@socketio.on('requestReadDataFromSource', namespace='/api/preprocessing')
def read_data_from_source(session_id, data):
    print('Read data from source')
    current_session = user_session.get_session_information(session_id)
    # selected_data_source_id = request.values['selectedDataSourceId']
    selected_data_source_id = int(
        data['data_source_id']) - 1  # -1 for zero based indexing of data_sources compared to 1 based indexing in db
    data_sources = get_all_data_sources()
    selected_source = data_sources[selected_data_source_id]

    dataframe = data_source_handler.read_from_source(selected_source)
    dataframe.to_csv(current_session['unmodified_data_location'], sep=";")
    dataframe.to_csv(current_session['data_location'], sep=";")

    # data_sources = get_all_data_sources()
    # pipeline_names = get_all_pipeline_names()
    emit('preprocessingStatus', {'task': 'read', 'result': 'success', 'data_source_name': selected_source.Name})
    return  # render_template('preprocessing/preprocessing.html', data_sources=data_sources, pipelines=pipeline_names)


@api_bp.route('/get_all_pipeline_names')
def get_all_pipeline_names():
    print('Get all pipeline names')
    projects_path = app.config['USER_PROJECT_DIRECTORY']
    projects_directories = (user_project_handler.get_all_user_projects(projects_path))
    return projects_directories


@socketio.on('requestProjectRun', namespace='/api/run_project')
def run_project_persistent_connection(session_id, data):
    session_information = user_session.get_session_information(session_id)
    project_name = data['projectName']
    pipeline_parameters = input_parser.parse_parameter_list(data['pipelineParameters'], '&;', ':=')
    emit('progressLog', {'message': f"Starting pipeline for project {project_name}"})

    project_module = user_project_handler.import_project_module(app.config['USER_PROJECT_DIRECTORY'], project_name)
    result_dataframe = user_project_handler.run_user_project(project_module,
                                                             session_information['unmodified_data_location'],
                                                             pipeline_parameters)

    result_dataframe.to_csv(session_information["data_location"], sep=";")
    emit('success', {'message': "Pipeline finished successfully"})

    return redirect(url_for('blueprints/process_mining.process_discovery'))


@socketio.on('requestDiscoveryPreparation', namespace='/api/run_process_discovery')
def prepare_discovery(session_id, xes_attribute_columns=None, filters=None, options=None):
    current_session = user_session.get_session_information(session_id)
    old_filters = current_session["pm_filters"]
    dataframe_key_metrics = {}
    try:
        dataframe = pd.read_csv(current_session["data_location"], index_col=0, sep=";")
    except FileNotFoundError:
        return

    column_names = list(dataframe.columns.values)

    # if no xes columns have ever been selected, just return all of the column names and nothing else
    if xes_attribute_columns == None and (
            bool(current_session['pm_xes_attributes']) == False or current_session['pm_xes_attributes'] == None):
        emit("updateColumnNames", column_names)
        return

    # if xes_attributes are given, update session info with the selected column names
    if not xes_attribute_columns == None:
        if xes_attribute_columns["timestamp_column"] == "None" or xes_attribute_columns["activity_column"] == "None" or \
                xes_attribute_columns["caseId_column"] == "None":
            emit("warning", {
                "message": "You shouled select at least Acitivity, Timestamp and Case ID columns in order to obtain valid event logs."})
            return
        user_session.update_session(session_id, "PMXesAttributes", xes_attribute_columns)

    # if filters are given, update session info with filters
    if not filters == None:
        user_session.update_session(session_id, "PMFilters", filters)

    # if filters are given, update session info with filters
    if not options == None:
        user_session.update_session(session_id, "PMOptions", options)

    current_session = user_session.get_session_information(session_id)

    # prepare dataframe by applying xes column names to selected columns
    dataframe = event_log_generator.prepare_event_log_dataframe(dataframe, current_session['pm_xes_attributes'])

    # generate event log dataframe (might be more reasonable to use the direct dataframe -> eventlog conversion without storing to file first)
    dataframe.to_csv(current_session["process_mining_data_location"],
                     sep=';')  # TODO might be better do directly convert the dataframe to evenglog rather than saving to disk!

    event_log = event_log_generator.generate_xes_log(current_session["process_mining_data_location"], separator=';')

    # apply filters and update dataframe if there are filters selected
    if current_session["pm_filters"]:

        # set filters and filter options
        event_log = filter_handler.apply_all_filters(event_log, current_session["pm_filters"])

        from pm4py.objects.conversion.log import converter as log_converter

        # refresh the dataframe
        dataframe_filtered = log_converter.apply(event_log, variant=log_converter.Variants.TO_DATA_FRAME)
        # check if the resulting dataframe still has enough information to create a valid porcess model
        if "time:timestamp" not in dataframe_filtered.columns or \
                "concept:name" not in dataframe_filtered.columns or \
                "case:concept:name" not in dataframe_filtered.columns:
            # if not, reset the old filters are some and dont use the filtered dataframe
            if old_filters:
                user_session.update_session(session_id, "PMFilters", old_filters)
            emit("warning", {"message": "The selected filters did not yield a valid process model."})
            return
        # else use the updated data frame
        else:
            dataframe = dataframe_filtered

    # Extract function for getting all the possible values for the pm filters
    pm_filter_options = {}
    timestamp_options = {}

    # TODO problem: if you refresh activity options after already applying some activity options, you will probably no more able to select form the entire range of activities, but the reduction in options is on the other hand required after start time and end time change
    from pm4py.algo.filtering.log.start_activities import start_activities_filter
    from pm4py.algo.filtering.log.end_activities import end_activities_filter
    from pm4py.algo.filtering.log.cases import case_filter

    start_activities = list(start_activities_filter.get_start_activities(event_log).keys())
    end_activities = list(end_activities_filter.get_end_activities(event_log).keys())
    pm_filter_options["start_activity_options"] = start_activities
    pm_filter_options["end_activity_options"] = end_activities

    timestamp_column = dataframe["time:timestamp"]
    min_time = timestamp_column.min()
    max_time = timestamp_column.max()
    timestamp_options["min"] = min_time.strftime("%d-%b-%Y %H:%M:%S") if (
        isinstance(min_time, datetime.datetime)) else min_time
    timestamp_options["max"] = max_time.strftime("%d-%b-%Y %H:%M:%S") if (
        isinstance(max_time, datetime.datetime)) else max_time
    pm_filter_options["timestamp_options"] = timestamp_options
    # maybe add min and max cost as well

    case_concept_names = list(dataframe['case:concept:name'].unique())
    pm_filter_options["case_id_options"] = case_concept_names

    dataframe_key_metrics = process_discovery.get_dataframe_key_metrics(dataframe, event_log,
                                                                        current_session['pm_xes_attributes'])

    from pm4py.objects.log.exporter.xes import exporter as xes_exporter
    xes_exporter.apply(event_log, current_session['event_log_location'])

    dataframe.to_csv(current_session["process_mining_data_location"], sep=";")

    emit("processDiscoveryUpdateEverything", {"all_column_names": column_names,  # all column names of the data frame
                                              "pm_xes_attributes": current_session['pm_xes_attributes'],
                                              # selected xes attribute columns
                                              "pm_filter_options": pm_filter_options,
                                              # get all possible values for the process mining filters
                                              "pm_filters": current_session['pm_filters'],  # selected filters
                                              "pm_options": current_session['pm_options'],
                                              # selected options regarding the output of the discovery
                                              "pm_dataframe_key_metrics": dataframe_key_metrics})  # key metrics such as number of cases and events

    return


def process_discovery_thread_wrapper(current_session, options, results):
    results.append(process_discovery.run(current_session, options))
    result_dataframe = pd.read_csv(current_session["data_location"],index_col=0, sep=";")
    df1 = result_dataframe[['Type','Operation']]
    prev_action_seq1 = ['View Project', 'Project Create', 'Add Project']
    next_action_seq1 = ['Open Project', 'Project', 'View Project']
    KPI = 0.5
    #conformance_handler.check_comformance(result_dataframe,prev_action_seq1,next_action_seq1,KPI)
    return results


@socketio.on('requestProcessDiscovery', namespace='/api/run_process_discovery')
def run_process_discovery(session_id, options):
    emit('info', {"message": "Starting process mining"})
    user_session.update_session(session_id, "PMOptions", options)

    import threading

    current_session = user_session.get_session_information(session_id)
    # process_model = process_discovery.run(current_session, options)

    results = []

    # use parallelization to run the texing logics in a separate threat. TODO Is not supported on development server, needs to be veryified on productive server.
    threading.Thread(target=process_discovery_thread_wrapper, args=(current_session, options, results)).start()

    import time
    while not (results):
        time.sleep(2)

    process_model = results[0]
    emit(process_model[0], process_model[1])

    #check_comformance(result_dataframe)
    return


@socketio.on('requestDiscoveryReset', namespace='/api/run_process_discovery')
def reset_discovery(session_id):
    # update the stored session with empty attributes to override any existing values
    user_session.update_session(session_id, "PMXesAttributes", "")
    user_session.update_session(session_id, "PMFilters", "")

    prepare_discovery(session_id)
    return


@socketio.on('requestFilterReset', namespace='/api/run_process_discovery')
def reset_discovery_filters(session_id):
    user_session.update_session(session_id, "PMFilters", "")

    prepare_discovery(session_id)
    return


@api_bp.route('/download_temporary_data', methods=['GET'])
def download_temporary_data():
    session_id = request.args["session_id"]
    requested_file = request.args["requested_file"]

    current_session = user_session.get_session_information(session_id)
    path = file_handler.get_download_path(current_session, requested_file)

    return send_file(path, as_attachment=True)

##ConformanceChecking ..added by Mrunmai
@api_bp.route('/conformance_checking', methods=['GET','POST'])
#@socketio.on('requestReadOperationSeqSet', namespace='/api/conformance')
def conformance_checking():
    print('api/conformance')
    session_id = request.args.get("session_id")
    current_session = user_session.get_session_information(session_id)
    print('New1',session_id)
    opSeqSet1 = (request.form['OpSeqSet1']).split(",")
    #opSeqSet1 = data['op_seq_set1']
    print('New2', opSeqSet1)
    print(opSeqSet1[0])
    opSeqSet2 = (request.form['OpSeqSet2']).split(",")
    print('New3', type(opSeqSet2))
    print(opSeqSet2[0])
    performance = request.form['performance']
    print('New4', performance)
    print('new5',type(performance))
    result_dataframe = pd.read_csv(current_session["data_location"], index_col=0, sep=";")
    print('result_dataframe',result_dataframe)
    #df1 = result_dataframe[['Type', 'Operation']]
    #prev_action_seq1 = ['View Project', 'Project Create', 'Add Project']
    #next_action_seq1 = ['Open Project', 'Project', 'View Project']
    #KPI = 0.5
    conformance_handler.check_comformance(result_dataframe, opSeqSet1, opSeqSet2, performance)


    return redirect(url_for('blueprints/conformance_checking.conformance_checking'))