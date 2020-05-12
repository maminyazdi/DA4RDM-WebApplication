import pandas as pd
import numpy as np
import json
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

#    dataframe = pd.read_csv(config.current_session["data_location"], sep=";")

#    dataframe = dataframe.dropna()

    dataframe = parse_message(dataframe)
    dataframe.to_csv("C:\Temp\csv2after_message_parsed.csv")
    dataframe['Timestamp'] = pd.to_datetime(dataframe['Timestamp'], utc=True)

    dataframe = dataframe.sort_values(by="Timestamp")
    dataframe.dropna()

    dataframe = create_session_ids(dataframe, 30)

    dataframe.Timestamp = dataframe.Timestamp.dt.strftime("%YYYY-%MM-%DD %hh:%mm:%ss.%3")
    dataframe.Timestamp = dataframe.Timestamp.str.slice(0, 23)

    dataframe.to_csv("C:\Temp\da4dsuserframes\combined_time_string.csv")
    dataframe = xes_formatter.prepare_xes_columns(dataframe, 3, 1, 2, 6)

    # TODO treat inconsistencies and missing values
    dataframe.to_csv("C:\Temp\csv3xes_and_cleaning")
    dataframe.to_csv(config.current_session["data_location"])

    return render_template('main/index.html')

def parse_message(dataframe):
    """parses the "message" column from the Log dataframe and returns a dataframe with the columns parsed from the json contents of Message."""
    #some flawed log entries contain an error message instead of the desired log message and should be cleaned (here: removed)
    dataframe = dataframe[~dataframe.Message.str.contains("Executed action method")]
    message_dataframe = pd.io.json.json_normalize(dataframe.Message.apply(json.loads))

    return message_dataframe

def create_session_ids(dataframe, threshold):
    """Creates session ids by first grouping rows by userId, then detects rows belonging to distinct session by checking
    if any two consecutive rows are further apart from each other than threshold minutes"""

    user_ids = dataframe.UserId.unique()
    new_column_index = len(dataframe.columns)
    return_dataframe = pd.DataFrame()

    #generate dataframes containing all rows of one user id for each user id
    for user_id in user_ids:
        user_dataframe = dataframe.query(f"UserId == '{user_id}'")

        time_diff_series = user_dataframe.Timestamp - user_dataframe.Timestamp.shift()
        threashold_check_series = time_diff_series > pd.Timedelta(value=threshold, unit='m')

        session_id_column = (user_dataframe.UserId[threashold_check_series] + user_dataframe.Timestamp[threashold_check_series].dt.strftime("%d-%m-%Y %H:%M:%S"))

        user_dataframe["SessionIdCalculated"] = session_id_column

        user_dataframe.iloc[0, new_column_index] = user_dataframe.iloc[0, 3] + user_dataframe.iloc[0, 2].strftime("%d-%m-%Y %H:%M:%S")

        user_dataframe.SessionIdCalculated = user_dataframe.SessionIdCalculated.ffill()

        return_dataframe = pd.concat([return_dataframe, user_dataframe], axis=0, join='outer', ignore_index=True, keys=None,
          levels=None, names=None, verify_integrity=False, copy=True)

    #maybe sort the resultring dataframe again

    return_dataframe.to_csv("C:\Temp\da4dsuserframes\combined.csv")

    return return_dataframe
