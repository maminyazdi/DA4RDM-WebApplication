import dask.dataframe as dd
from flask_socketio import emit

def execute(source_path, delimiter=";"):
    """retreive a dataframe from a csv file
    for additional possible options refer to [Dask Api](https://docs.dask.org/en/latest/dataframe-api.html#dask.dataframe.read_csv)"""
    emit('progressLog', {'message': "reading from csv file"})

    df = dd.read_csv(source_path, delimiter=delimiter, parse_dates=True)
    return df