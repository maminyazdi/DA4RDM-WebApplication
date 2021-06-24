import pandas as pd
from flask_socketio import emit

def execute(left_column, right_column):
    """Creates a cross matrix for two columns/series objects. IMPORTANT: This currently uses pandas as underlying framework and thus returns a pandas dataframe (and is limited by the memory etc. restrictions that concern pandas.

    Args:
        left_column (pandas.series): One of the columns to use for the transformation.
        right_column (pandas_series): One of the columns to use for the transformation.

    Returns:
        dataframe (dataframe)
    """

    emit('progressLog', {'message': "Creating cross matrix."})

    cross_matrix = pd.crosstab(left_column, right_column, rownames=left_column, colnames=right_column)
    return cross_matrix
