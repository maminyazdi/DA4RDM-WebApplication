import pandas as pd
from flask_socketio import emit

def execute(dataframe):
    """Serializes a dataframe to JSON. IMPORTANT: This expects a pandas dataframe for now."""

    emit('progressLog', {'message': "Serializing dataframe as json."})

    json = dataframe.to_json(orient='split')
    return json