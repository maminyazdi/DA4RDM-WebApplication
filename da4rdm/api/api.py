import os
import re
import csv
import sqlalchemy
import datetime
import uuid
import pandas as pd
import json
from flask_socketio import emit
from pm4py.algo.filtering.log.attributes import attributes_filter
from pm4py.algo.filtering.log.variants import variants_filter

from da4rdm import socketio

from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, jsonify, current_app as app, send_from_directory,
    send_file,make_response
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from da4rdm import db, Config
from da4rdm.models import (InflexibleDataSourceConnection, DataBaseDialect, DialectParameters, DataSource,SessionInformation)
from da4rdm.api.data_source import data_source_handler
from da4rdm.api.process_mining import (process_discovery, event_log_generator, filter_handler,conformance_handler)
from da4rdm.api.preprocessing import user_project_handler
from . import (user_session, input_parser, file_handler)
from da4rdm import conformanceChecking

api_bp = Blueprint('blueprints/api', __name__, template_folder='templates', static_folder='static')

"""API methods handle incoming requests and also take care of sesison and authentication related tasks at the highest level."""


@socketio.on('create_new_session', namespace='/api/create_new_session')
def create_new_session():
    session_id = user_session.create_new_session()
    emit('session',
         session_id)  # TODO maybe use simple http request instead of socket or find a way to wait for the response
    global temp_id
    temp_id = session_id
    #vis()
    return session_id


@api_bp.route('/api/get_all_data_sources')
def get_all_data_sources():
    data_sources = db.session.query(DataSource).all()
    return data_sources


@api_bp.route('/new_data_source', methods=['POST'])
def new_data_source():
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
    # Added for getting session_id for get_unique_operations() method

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


# For fetching list of unique operations based on Activity column
@api_bp.route('/api/get_unique_operations')
def get_unique_operations():
    current_session = user_session.get_session_information(temp_id)
    xes_attributes = current_session['pm_xes_attributes']
    if bool(xes_attributes):
        activity_col = xes_attributes["activity_column"]
        result_dataframe = pd.read_csv(current_session["data_location"], index_col=0, sep=";")
        df = pd.unique(result_dataframe[activity_col])
        df.sort()
    else:
        df = []
    return df


# socket for invoking ConformanceChecking method
@socketio.on('requestReadOperationSeqSet', namespace='/api/conformance')
def conformance_checking(session_id, action1, action2, data):
    current_session = user_session.get_session_information(session_id)
    operation_seq1 = action1.split(",")
    operation_seq2 = action2.split(",")
    eventually_followed_flg_val = data['eventuallyFollowedFlg']

    mins = data['min']
    sec = data['sec']
    # check for empty Mins and Sec field
    total_time = ((float(mins)*60) + float(sec)) if((mins != '') & (sec != '')) else ''
    print('total_time', type(total_time), total_time)
    result_dataframe = pd.read_csv(current_session["data_location"], index_col=0, sep=";")

    # Calling Conformance Check method based on Eventually Followed By checkbox
    json_result, non_conforming_cases, total_no_of_cases, dataset_start_time, dataset_end_time = \
        conformance_handler.conformance_eventually_followed_by(result_dataframe, operation_seq1[:len(operation_seq1)-1],
                                                               operation_seq2[:len(operation_seq2)-1], total_time) \
        if eventually_followed_flg_val \
        else conformance_handler.check_conformance(result_dataframe, operation_seq1[:len(operation_seq1)-1],
                                                   operation_seq2[:len(operation_seq2)-1], total_time)

    emit("conformanceCheckingOP", {"NonConformingCases": non_conforming_cases,
                                   "dataSet_start_time": dataset_start_time,
                                   "dataSet_end_time": dataset_end_time,
                                   "JSON_Response": json_result,
                                   "TotalNoOfCases": total_no_of_cases,
                                    })

    return


@api_bp.route('/api/get_unique_projects')
def get_unique_projects():
    import math
    data = pd.read_csv(r"C:\Users\ph-admin\PycharmProjects\da4rdm-conformance\da4rdm\api\test_data.csv", index_col=0, sep=";")
    """ TODO start ------
    current_session = user_session.get_session_information(temp_id)
    result_dataframe = pd.read_csv(current_session["data_location"], index_col=0, sep=";")
    df = pd.unique(result_dataframe.ProjectId)
    print('rdf',df)
    start = []
    end = []
    for i in range(len(df) - 1):

        project_filtered = list(result_dataframe[result_dataframe.ProjectId == df[i+1]].Timestamp)
        project_filtered.sort()
        #print(project_filtered)
        start.append(project_filtered[0])
        end.append(project_filtered[-1])
    print('s12',start)
    print('e12',end)
    -------- END """
    unique_project_id = pd.unique(data.ProjectId)

    return unique_project_id

@socketio.on('visualizationTest', namespace='/api/visualization')
def vis(sessionId,project_list,start_date,end_date,options):
    import numpy as np
    from datetime import datetime
    from scipy.stats import pearsonr
    from numpy.linalg import norm
    """ TODO Start -----
    print('session',sessionId)
    current_session = user_session.get_session_information(sessionId)
    result_dataframe = pd.read_csv(current_session["data_location"], index_col=0, sep=";")
    u_project = pd.unique(result_dataframe.ProjectId)
    print('u_project', u_project)
    ---END """
    print('Inside vis', project_list)
    print('date',type(start_date),start_date)
    start = datetime.strptime(start_date,'%Y-%m-%d')
    end = datetime.strptime(end_date,'%Y-%m-%d')
    print('start',start,end)
    project_id_list = project_list.split(",")
    print('project_id_list',project_id_list)
    #datafile = open(r"C:\Users\ph-admin\PycharmProjects\da4rdm-conformance\da4rdm\api\test_data.csv")
    #data = pd.DataFrame.from_dict(datafile)
    data = pd.read_csv(r"C:\Users\ph-admin\PycharmProjects\da4rdm-conformance\da4rdm\api\test_data.csv", index_col=0,sep=";")
    print('data', data)
    sheet = pd.read_excel(r"C:\Users\ph-admin\PycharmProjects\da4rdm-conformance\da4rdm\api\RDLC_Vector_Metrices - Copy.xlsx",sheet_name='Sheet1')

    dict1 = {}
    list1 = []
    # sorted_df = data.sort_values(by=['ProjectId'])
    unique_project_id = pd.unique(data.ProjectId)
    # print('vis_data',sorted_df[['Type','Operation','Timestamp','ProjectId']])
    operation_list = list(sheet.Operations)
    print('operation_list', type(operation_list), operation_list)
    for project_id in range(len(project_id_list)-1):
        print('PR',project_id_list[project_id])
        example_dataset_full = []
        example_dataset_binary__full = []
        p_op = []
        p_op1 = []
        cos_sim_list = []
        cos_sim_list1 = []
        df = time_df(data,project_id_list,project_id,start,end)
        example_dataset = np.zeros(len(operation_list))
        example_dataset_binary = np.zeros(len(operation_list))
        # print('example_dataset', example_dataset)
        #pdf = data[data.ProjectId == project_id_list[project_id]][['Operation','Timestamp']]
        #print('pdf',pdf)
        project_filtered_df = list(df.Operation)
        #project_filtered_df = list(data[data.ProjectId == project_id_list[project_id]].Operation)
        print('project_filtered_df',project_filtered_df)


        for j in range(len(project_filtered_df)):
            #print('project_filtered_df[j]', project_filtered_df[j])
            if (project_filtered_df[j] in operation_list):
                #print('index', operation_list.index(project_filtered_df[j]))
                index_of_op = operation_list.index(project_filtered_df[j])
                example_dataset[index_of_op] = example_dataset[index_of_op] + 1
                example_dataset_binary[index_of_op] = 1
                # print('example_dataset_update', example_dataset)
        example_dataset_full.append(example_dataset)
        example_dataset_binary__full.append(example_dataset_binary)
        print('example_dataset_full', example_dataset_full)
        print('example_dataset_binary__full', example_dataset_binary__full)
        print('options',options["PearsonWeighted"],options["PearsonBinary"],options["CosineWeighted"],options["CosineBinary"])
        if options["PearsonWeighted"]:
            print('PW')
            corr_list = pearson_corr(sheet, example_dataset)
            p_op = normlize(corr_list)
        if options["PearsonBinary"]:
            print('PB')
            corr_list1 = pearson_corr(sheet, example_dataset_binary)
            p_op1 = normlize(corr_list1)
        if options["CosineWeighted"]:
            print('CW')
            cos_sim_list = cosine_similarity(sheet, example_dataset)
        if options["CosineBinary"]:
            print('PB')
            cos_sim_list1 = cosine_similarity(sheet, example_dataset_binary)

        print('normalized',p_op,p_op1,cos_sim_list,cos_sim_list1)
        dict1 = {"pearson_weighted": p_op,
                    "pearson_binary":p_op1,
                    "cosine_similarity": cos_sim_list,
                    "cosine_similarity_binary": cos_sim_list1,
                                     }
        print('dict1',dict1)
        list1.append(dict1)
        print('list1',list1)

    emit("radarChart", {"Similarity_Response":list1})

    return


def pearson_corr(sheet,dataset):
    from scipy.stats import pearsonr

    corr1, _ = pearsonr(list(sheet.Planning), dataset)
    corr2, _ = pearsonr(list(sheet.Production), dataset)
    corr3, _ = pearsonr(list(sheet.Analysis), dataset)
    corr4, _ = pearsonr(list(sheet.Archival), dataset)
    corr5, _ = pearsonr(list(sheet.Access), dataset)
    corr6, _ = pearsonr(list(sheet['Re-Use']), dataset)
    corr_list = [corr1, corr2, corr3, corr4, corr5, corr6]
    return corr_list

def cosine_similarity(sheet,example_dataset):
    from numpy.linalg import norm
    import numpy as np
    cos_sim1 = np.dot(list(sheet.Planning), example_dataset) / (norm(list(sheet.Planning)) * norm(example_dataset))
    cos_sim2 = np.dot(list(sheet.Production), example_dataset) / (norm(list(sheet.Production)) * norm(example_dataset))
    cos_sim3 = np.dot(list(sheet.Analysis), example_dataset) / (norm(list(sheet.Analysis)) * norm(example_dataset))
    cos_sim4 = np.dot(list(sheet.Archival), example_dataset) / (norm(list(sheet.Archival)) * norm(example_dataset))
    cos_sim5 = np.dot(list(sheet.Access), example_dataset) / (norm(list(sheet.Access)) * norm(example_dataset))
    cos_sim6 = np.dot(list(sheet['Re-Use']), example_dataset) / (norm(list(sheet['Re-Use'])) * norm(example_dataset))
    cos_sim_list = [cos_sim1, cos_sim2, cos_sim3, cos_sim4, cos_sim5, cos_sim6]
    return cos_sim_list


def normlize(list1):
    op = []
    for i in range(len(list1)):
        #op.append((list1[i] - min(list1))/(max(list1) - min(list1)))
        op.append((list1[i] - (-1)) / 2)
    print('norm',op)

    return op

def time_df(data,project_id_list,project_id,start,end):
    from datetime import datetime
    dataframe = pd.DataFrame()
    pdf = data[data.ProjectId == project_id_list[project_id]]
    for i in range(len(pdf)):
        time = datetime.strptime(pdf.Timestamp.iloc[i],'%Y-%m-%d %H:%M:%S.%f')
        print('time',time,start,end)
        if (time >= start) and (time <= end):
            print('iloc',pdf.iloc[i])
            dataframe = dataframe.append(pdf.iloc[i])

    #print('dataframe',dataframe[['ProjectId','Timestamp']])
    return dataframe




