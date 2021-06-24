import os
import uuid
from flask import flash
from werkzeug.utils import secure_filename
from da4rdm.models import DataSource
from . import strategies
import pandas as pd
from da4rdm import db, Config

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'txt', 'csv', 'xes'}

    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def add_datasource(name_value, parameters_value, type_value, last_modified_value, file_data):

    data_source = DataSource()
    data_source.Name         = name_value
    data_source.Parameters   = parameters_value
    data_source.Type         = type_value
    data_source.LastModified = last_modified_value

    if data_source.Type == 'csv':
        data_source.Parameters = add_file(file_data, data_source.Parameters)
    elif data_source.Type == 'xes':
        data_source.Parameters = add_file(file_data, "")

    data_source.StoredOnServer = True
    db.session.add(data_source)
    db.session.commit()

    return

def add_file(file_data, data_source_parameters=""):
    """Saves a file to the data source location specified in Config.UPLOADED_USER_DATA_LOCATION and adds the path to the data source data base item.
    parameters:
        file_data: File data as coming from an upload form's post-request,
        data_source_parameters: Already set parameters required to read from the data source, default = "";
    returns:
        string: the data source parameters with the file location appended as "path:=<paht>"
    """
    if 'file' not in file_data:
        raise FileNotFoundError("No file part")
    file = file_data['file']
    if file.filename == '':
        raise FileNotFoundError("No selected file")
    if file and allowed_file(file.filename):
        filename = str(uuid.uuid4()) + "-" + secure_filename(file.filename).split(".")[0] + ".csv"
        file.save(os.path.join(Config.UPLOADED_USER_DATA_LOCATION, filename))
        # add file location to parameter list, which is technically not necessary but is kept to keep the flexible implementation of the csv reader
        path_key = "&;path:=" if (":=" in  data_source_parameters) else "path:=" # check if the handed parameters already contain one serialized key value pair
        data_source_parameters = data_source_parameters + path_key + Config.UPLOADED_USER_DATA_LOCATION + '/' + filename
        return data_source_parameters

def read_from_source(data_source):
    """Selects an data source handler based on the input data and uses it to generate a pandas data frame."""
    reading_strategy = strategies.getReadingStrategy(data_source.Type, data_source.StoredOnServer)
    dataframe = reading_strategy.generate_dataframe(data_source.Parameters)

    return dataframe