import os
import re
import csv
import sqlalchemy
import importlib
import datetime
from flask_socketio import emit
from da4ds import socketio


from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, jsonify, current_app as app
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from da4ds import db
from da4ds.models import ( InflexibleDataSourceConnection, DataBaseDialect, DialectParameters, DataSource )

api_bp = Blueprint('blueprints/api', __name__, template_folder='templates', static_folder='static')

@api_bp.route('/get_all_data_sources')
def get_all_data_sources():
    #TODO veryfy user permissons to access the data sources
    data_sources = db.session.query(DataSource).all()
    return data_sources

@api_bp.route('/new_data_source', methods=['POST'])
def safe_new_data_source():
    # TODO add form validation & escaping
    # generate a new data source entry in the app database
    data_source = DataSource()
    data_source.Name = request.form['dataSourceName']
    data_source.Parameters = request.form['dataSourceParameters']
    data_source.Type = "csv"
    data_source.LastModified = datetime.datetime.now()
    data_source.StoredOnServer = True
    db.session.add(data_source)
    db.session.commit()

    return render_template('main/index.html')

@api_bp.route('/read_data_from_source', methods=['POST'])
def read_data_from_source():
    data_sources = get_all_data_sources()
    selected_source = data_sources[int(request.values['selectedDataSourceId'])]

    dataframe = handle_source(selected_source)

    return dataframe

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
def run_project_persistent_connection(data):
    project_name = data['projectName'] # programmatically get the package and module names to import from the given project name
    emit('progressLog', {'message': f"Starting pipeline for project { project_name }"})
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
    emit('json', response)
    return #response

@socketio.on('requestProcessDiscovery', namespace='/api/run_process_discovery')
def run_process_discovery():
    emit('json', {"message": "Hello World!"})

    #####
    import pandas as pd
    import os
    import re
    from pm4py.objects.log.adapters.pandas import csv_import_adapter
    from pm4py.objects.conversion.log import factory as conversion_factory
    dataframe = csv_import_adapter.import_dataframe_from_path(os.path.join("C:/Users/qb268076/seminar/datasources/prepared4pm4py", "xesReadyFormatLog.csv"), sep=",")

    dataframe = dataframe.replace(to_replace="'time\:timestamp'\:Timestamp\(", value="", regex=True)
    dataframe = dataframe.replace(to_replace="\)", value="", regex=True)
    dataframe = dataframe.replace(to_replace="-[0-9]+-", value="/", regex=True)
    dataframe = dataframe.replace(to_replace="/[0-9]+ ", value=" ", regex=True)
    dataframe["time:timestamp"] = pd.to_datetime(dataframe["time:timestamp"], utc=True)

    from pm4py.algo.filtering.pandas.timestamp import timestamp_filter
    df_timest_events = timestamp_filter.apply_events(dataframe, "2020-01-01 00:00:00", "2020-02-02 23:59:59")
    log = conversion_factory.apply(dataframe)

    from pm4py.algo.discovery.dfg import factory as dfg_factory
    dfg = dfg_factory.apply(log)

    from pm4py.visualization.dfg import factory as dfg_vis_factory
    gviz = dfg_vis_factory.apply(dfg, log=log, variant="frequency")

    api_file_path = os.path.abspath(os.path.dirname(__file__))
    #pattern = re.compile(r"api[/\\\\]+$")
    #path = pattern.sub("static\\images\\est.gv.png", api_file_path)
    path = api_file_path.replace("api", "static\\images\\test.gv.png") # TODO replace static file path
    dfg_vis_factory.save(gviz, path)
    emit('gviz', "../static/images/test.gv.png") # TODO replace static file path
    #dfg_vis_factory.view(gviz)

    #emit('gviz', dfg_vis_factory.view(gviz))
    #####

    return gviz
