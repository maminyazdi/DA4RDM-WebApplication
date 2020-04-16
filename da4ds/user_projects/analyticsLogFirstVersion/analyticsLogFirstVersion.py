import pandas as pd
import numpy as np
from flask_socketio import emit
from da4ds import socketio
from flask import (
    render_template, jsonify, current_app as app
)

def run(config):
    dataframe = pd.read_csv(config.current_session["data_location"], sep=";")

    print(dataframe.head())

    dataframe = parse_message(dataframe)

    # dataframe = prepare_timestamp_column(dataframe, 1)
    # dataframe = prepare_case_colum(dataframe, 2)
    # dataframe = prepare_resource_column(dataframe, 3)
    # dataframe = prepare_activitiy_column(dataframe, 4)

    # print(dataframe.head(20))

    # #### this are the known modifications that were down after the data was 'xes ready'
    # #dataframe = config.data
    # dataframe = dataframe.replace(to_replace="'time\:timestamp'\:Timestamp\(", value="", regex=True)
    # dataframe = dataframe.replace(to_replace="\)", value="", regex=True)
    # dataframe = dataframe.replace(to_replace="-[0-9]+-", value="/", regex=True)
    # dataframe = dataframe.replace(to_replace="/[0-9]+ ", value=" ", regex=True)
    # dataframe["time:timestamp"] = pd.to_datetime(dataframe["time:timestamp"], utc=True)

    # ###TESTCODE
    # print(dataframe.head(20))

    # #dataframe.to_csv("C:/Temp/da4ds_temp1.csv")
    # dataframe.to_csv(config.current_session["data_location"])

    # return render_template('main/index.html')


def prepare_timestamp_column(dataframe, column_index):
    #prepare_head
    column_head = dataframe.columns.values

    if not column_head[column_index].startswith("time:timestamp"):
        column_head[column_index] = "time:timestamp" + column_head[column_index]
        dataframe.columns = column_head
        #new_column_name = "time:timestamp" + column_head[column_index]
        #column_head = column_head.insert(column_index, new_column_name)
        #print(column_head)

    print(dataframe.head(20))

    #prepare_values
    #column = dataframe.iloc[:, column_index]

    column_name = column_head[column_index]

    dataframe[column_name] = np.where((not str(dataframe[column_name]).startswith("'time:timestamp':Timestamp('")),"'time:timestamp':Timestamp('" + dataframe[column_name] + "')",dataframe[column_name])
    #dataframe[column_name] = dataframe.applymap(lambda element: element if str(element).startswith("'time:timestamp':Timestamp('") else ("'time:timestamp':Timestamp('" + dataframe[column_name] + "')")) #TODO fing more efficient way

    print("-------")
    print(dataframe.head(20))

    print(dataframe.shape)

    return dataframe

def prepare_case_colum(dataframe, column_index):
    #prepare_head
    column_head = dataframe.columns.values
    if not column_head[column_index].startswith("case:concept:name"):
        column_head[column_index] = "case:concept:name"# + column_head[column_index]
        dataframe.columns = column_head
    #prepare_values

    column_name = column_head[column_index]

    dataframe[column_name] = np.where((not str(dataframe[column_name]).startswith("'case:concept:name'")),"'case:concept:name': '" + dataframe[column_name] + "'",dataframe[column_name])

    return dataframe

def prepare_resource_column(dataframe, column_index):
    #prepare_head
    column_head = dataframe.columns.values
    if not column_head[column_index].startswith("org:resource"):
        column_head[column_index] = "org:resource" + column_head[column_index]
        dataframe.columns = column_head
    #prepare_values

    column_name = column_head[column_index]

    dataframe[column_name] = np.where((not str(dataframe[column_name]).startswith("'org:resource'")),"'org:resource': '" + dataframe[column_name] + "'",dataframe[column_name])

    print(dataframe.head(20))

    return dataframe

def prepare_activitiy_column(dataframe, column_index):

    column_head = dataframe.columns.values
    if not column_head[column_index].startswith("concept:name"):
        column_head[column_index] = "concept:name"# + column_head[column_index]
        dataframe.columns = column_head

        return dataframe

def parse_message(dataframe):

    message_contents = dataframe.message

    return dataframe