import pandas as pd
from flask_socketio import emit
from da4ds import socketio
from flask import (
    render_template, jsonify, current_app as app
)

def run(config):
    dataframe = pd.read_csv(config.current_session["data_location"])

    dataframe = prepare_timestamp_column(dataframe)
    dataframe = prepare_case_colum(dataframe)
    dataframe = prepare_resource_column(dataframe)


    #### this are the known modifications that were down after the data was 'xes ready'
    #dataframe = config.data
    dataframe = dataframe.replace(to_replace="'time\:timestamp'\:Timestamp\(", value="", regex=True)
    dataframe = dataframe.replace(to_replace="\)", value="", regex=True)
    dataframe = dataframe.replace(to_replace="-[0-9]+-", value="/", regex=True)
    dataframe = dataframe.replace(to_replace="/[0-9]+ ", value=" ", regex=True)
    dataframe["time:timestamp"] = pd.to_datetime(dataframe["time:timestamp"], utc=True)

    #dataframe.to_csv("C:/Temp/da4ds_temp1.csv")
    dataframe.to_csv(config.current_session["output_location"])

    return render_template('main/index.html')


def prepare_timestamp_column(dataframe, column_index):
    #prepare_head
    column_head = dataframe.columns
    if not column_head[column_index].startswith("time:timestamp"):
        column_head[column_index] = "time:timestamp" + column_head[column_index]
    #prepare_values
    column = dataframe[column_index]

    return dataframe

def prepare_case_colum(dataframe, column_index):
    #prepare_head
    column_head = dataframe.columns
    if not column_head[column_index].startswith("case:concept:name"):
        column_head[column_index] = "case:concept:name" + column_head[column_index]
    #prepare_values

    return dataframe

def prepare_resource_column(dataframe, column_index):
    #prepare_head
    column_head = dataframe.columns
    if not column_head[column_index].startswith("org:resource"):
        column_head[column_index] = "org:resource" + column_head[column_index]
    #prepare_values

    return dataframe

