from flask_socketio import emit

def execute(dataframe, column, method="ffill"):
    """Fills not availabe (na) entries in the selected dataframe column.

    Args:
        dataframe (dask.dataframe):
        column (string): The name of the column of the dataframe in which na values should be replaced.
        method (string): Method to use for filling holes in reindexed Series
            pad / ffill (default): propagate last valid observation forward to next valid
            backfill / bfill: use NEXT valid observation to fill gap

    Return:
        dask.dataframe with na values replaced
    """
    emit('progressLog', {'message': "Filling missing values."})

    dataframe[column] = dataframe[column].fillna(method=method)
    return dataframe