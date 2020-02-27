import dask.dataframe as dd
from flask_socketio import emit

def execute(dataframe, renamings):
    """Renames the specified columns of a data set.
    Renamings is a dictionary<string, string> mapping the old column names to the new ones for all columns that should be renamed

    Args:
        dataframe (dask.dataframe): The dataframe whose column labels should be renamed.
        renamings (dict<str, str>): A dictionary containing the old names as keys and the new names as columns. Only column labels found within this dictionary will be renamed; other columns will keep their old name.

    Returns:
        dask.dataframe with the renamed columns.
    """

    emit('progressLog', {'message': "Renaming columns."})

    columns = dataframe.columns
    new_columns = [renamings[_] if _ in renamings else _ for _ in columns]
    updated_df = dataframe.rename(columns=dict(zip(columns, new_columns)))
    return updated_df