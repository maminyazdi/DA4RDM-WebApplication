import dask.dataframe as dd
from flask_socketio import emit

def execute(local_database, kind, index_col='Id'):
    """Get a dataframe for further work in the pipeline from the locally stored data"""

    emit('progressLog', {'message': "Reading from local database."})

    connection_string = str(local_database.engine.url)
    dataframe = dd.read_sql_table(table=kind, uri=connection_string, index_col=index_col)
    return dataframe