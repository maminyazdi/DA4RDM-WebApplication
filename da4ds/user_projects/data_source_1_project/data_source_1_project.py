import pandas as pd
from flask_socketio import emit
from da4ds import socketio
from flask import (
    render_template, jsonify, current_app as app
)

def run(config):
    #dataframe = config.data
    dataframe = pd.read_csv(config.current_session["data_location"])

    dataframe = dataframe.replace(to_replace="'time\:timestamp'\:Timestamp\(", value="", regex=True)
    dataframe = dataframe.replace(to_replace="\)", value="", regex=True)
    dataframe = dataframe.replace(to_replace="-[0-9]+-", value="/", regex=True)
    dataframe = dataframe.replace(to_replace="/[0-9]+ ", value=" ", regex=True)
    dataframe["time:timestamp"] = pd.to_datetime(dataframe["time:timestamp"], utc=True)

    #dataframe.to_csv("C:/Temp/da4ds_temp1.csv")
    dataframe.to_csv(config.current_session["output_location"])

    return render_template('main/index.html')