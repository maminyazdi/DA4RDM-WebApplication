import dask.dataframe as dd
from flask_socketio import emit

def execute(dataframe):
    """Drops all rows with null values.

    Args:
        dataframe (dask.dataframe): The dataframe on which to remove rows.

    Returns:
        dataframe (dask.dataframe)
    """
    emit('progressLog', {'message': "Dropping null rows."})

    return dataframe.dropna()
