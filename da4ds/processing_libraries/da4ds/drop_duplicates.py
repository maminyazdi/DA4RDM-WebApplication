import dask.dataframe as dd
from flask_socketio import emit
def execute(dataframe):
    """Drops duplicate rows from the dataframe."""
    emit('progressLog', {'message': "Dropping duplicate rows."})

    return dataframe.drop_duplicates()
