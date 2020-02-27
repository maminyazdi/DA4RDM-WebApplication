import dask.dataframe as dd
from flask_socketio import emit

def execute(source_connection_string, table_name, index_column):
    """Create a dataframe from sql database.

    Args:
        source_connection_string (str): The connection string which can be used by sqlAlchemy to connect to the database. For more information on how this string should be formatted, look here: https://docs.sqlalchemy.org/en/13/core/engines.html
        table_name (str): The name of the table within the database.
        index_column (int): The column to be used as index within the dataframe.

    Returns:
        dask.dataframe
    """

    emit('progressLog', {'message': "Reading from local database."})

    dataframe = dd.read_sql_table(table=table_name, uri=source_connection_string, index_col=index_column) #TODO functionality needs to be tested
    return dataframe