from flask_socketio import emit

from random import randrange

def remove_rows_from_index_list(dataframe, row_indeces):
    """Removes the rows with row_indeces from the dataframe.
    This relies on pandas dataframes for now.

    Args:
        dataframe (pandas.dataframe): The dataframe from which the rows should be removed.
        indeces (dict<int>): The indeces of which rows should be removed.
        n (int): The amount of times the selected rows should be appended to the dataframe.

    Returns:
        pandas.dataframe: The dataframe with the selected rows removed.
    """

    #TODO For the implementation for dask we could probably write a map apply function.
    emit('progressLog', {'message': "Removing rows."})

    index_list = [dataframe.index[x] for x in row_indeces]
    result_dataframe = dataframe.drop(index_list)
    return result_dataframe

def execute(dataframe, column_name, current_count, target_count):
    """Removes rows that originally occur at random for current_count amount of times in the dataframe until target_count is obtained.

    Args:
        dataframe (pandas.dataframe):
        column_name (string): The name of the column over which to aggregate.
        current_count (int): The count of the occurences of rows with the same values in the specified column in the dataframe.
        target_count (int): The targeted count for the remaining of the targeted rows after removal.

    Returns:
        dataframe: The dataframe with the rows removed.
    """

    emit('progressLog', {'message': "Removing rows."})

    rows_to_remove = dataframe[dataframe.groupby(column_name)[column_name].transform('size') == current_count]
    indeces = rows_to_remove.index

    index_list = indeces.values.tolist()
    index_list = [x-1 for x in index_list]

    for i in range(target_count):
        random_surviver = randrange(0, len(index_list), 1)
        del index_list[random_surviver]

    dataframe = remove_rows_from_index_list(dataframe, index_list)
    return dataframe
