import dask.dataframe as dd
from flask_socketio import emit

def execute(dataframe, column_name, new_column_name, new_column_rule):
    """Creates a new Column based on some calculation on another column of a dataframe."""

    emit('progressLog', {'message': "Adding column."})

    dataframe[new_column_name] = dataframe[column_name].apply(new_column_rule)

    pass