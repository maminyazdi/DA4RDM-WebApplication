import pandas as pd
import numpy as np
from flask_socketio import emit
from da4ds import socketio
from flask import (
    render_template, jsonify, current_app as app
)
from da4ds.processing_libraries.da4ds import xes_formatter

def run(config):
    import sqlalchemy

    engine = sqlalchemy.create_engine(config.SOURCE_CONNECTION_STRING)

    with engine.connect() as connection:
        dataframe = pd.read_sql(config.QUERY_SRTING, con=engine, index_col="Id")

        print(dataframe.head(20))

#    dataframe = pd.read_csv(config.current_session["data_location"], sep=";")

#    dataframe = dataframe.dropna()


    dataframe = parse_message(dataframe)
    dataframe['Timestamp'] = pd.to_datetime(dataframe['Timestamp'])

    print(dataframe.info())

    dataframe = dataframe.sort_values(by="Timestamp")
    dataframe.dropna()

    print(dataframe.head(20))

    dataframe = create_session_ids(dataframe, 60)

    # TODO prepare for pm4py

    dataframe = xes_formatter.prepare_xes_columns(dataframe, 3, 1, 2, 6)

    # TODO treat inconsistencies and missing values

    print(dataframe.head(20))

    # dataframe = prepare_timestamp_column(dataframe, 2)
    # dataframe = prepare_case_colum(dataframe, 3)
    # dataframe = prepare_activity_column(dataframe, 1)
    # dataframe = prepare_resource_column(dataframe, 6)

    dataframe.to_csv(config.current_session["data_location"])

    return render_template('main/index.html')

def parse_message(dataframe):
    """parses the "message" column from the Log dataframe and returns a dataframe with the columns parsed from the json contents of Message."""

    import json

    message_dataframe = pd.io.json.json_normalize(dataframe.Message.apply(json.loads))

    message_dataframe.to_csv("C:/Temp/aaaaexpectedparsedtest.csv")

    return message_dataframe

def create_session_ids(dataframe, threshold):
    """Creates session ids """

    user_ids = dataframe.UserId.unique()

    #generate dataframes containing all rows of one user id for each user id

    for user_id in user_ids:
        user_dataframe = dataframe.query(f"UserId == '{user_id}'")

        #user_dataframe.sessionId = pd.Timedelta(user_dataframe.UserId - user_dataframe.UserId.shift()).seconds / 60.0

        time_diff_series = user_dataframe.Timestamp - user_dataframe.Timestamp.shift()
        threashold_check_series = time_diff_series > pd.Timedelta(value=30, unit='m')

        c = (user_dataframe.UserId[threashold_check_series] + user_dataframe.Timestamp[threashold_check_series])

        print(c)

        user_dataframe.to_csv(f"C:/Temp/aaaaagarbo/{user_id}")

        print(user_dataframe.head(50), user_dataframe.tail(50))

    #assign session ids cia user id and timestamp with in accordance with the threshold for timestamp difference in consecutive rows



    #merge all the dataframes together



    #maybe sort the resultring dataframe again

    return dataframe
