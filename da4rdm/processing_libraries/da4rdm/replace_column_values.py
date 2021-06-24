from flask_socketio import emit
from da4rdm import socketio

def execute(df, column_name, regex_target, replacement_expression):
    """function

    Parameters
    ----------

    dataframe: dask.dataframe
        dataframe to work on
    column_names: string
        iterable of strings corresponding to the names of the target columns
    regex_target: regular expression string
        target regular expression. the exact match will be replaced in the specified columns
    replacement_expression: string
        the value by which the target expression gets replaced

    Returns
    -------

    dataframe: dask.dataframe
        new dataframe with the updated values

    """

    emit('progressLog', {'message': "Replacing column values."})


    updated_df = df.replace({column_name: regex_target}, {column_name: replacement_expression}, regex=True)
    return updated_df