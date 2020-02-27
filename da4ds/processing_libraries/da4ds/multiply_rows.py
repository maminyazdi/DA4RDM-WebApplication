from flask_socketio import emit

def execute(dataframe, column_name, current_count, factor=1):
    """Duplicates all rows that occur current_count times in the dataframe by appending them to its end factor times
    This relies on pandas dataframes for now.

    Args:
        dataframe (pandas.dataframe):
        column_name (str):
        current_count (int):
        factor (int):

    Returns:
        pandas.dataframe: The dataframe with the duplicate rows appended.
    """

    emit('progressLog', {'message': "Multiplying rows."})
    #TODO For the implementation for dask we could probably write a map apply function.

    rows_to_copy = dataframe[dataframe.groupby(column_name)[column_name].transform('size') == current_count]
    result_dataframe = dataframe.append(([rows_to_copy] * factor), ignore_index=True)
    return result_dataframe