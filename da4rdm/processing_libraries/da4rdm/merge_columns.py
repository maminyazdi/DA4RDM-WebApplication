import numpy as np
import dask.dataframe as dd
from flask_socketio import emit

def execute(dataframe, merge_column_left, merge_column_right, target_column, prefix = '', separator = ''):
    """Merges two columns into a new column and adds the new column to the dataframe."""

    emit('progressLog', {'message': "Mergin columns."})

    result_frame = dataframe.apply(merge_values, axis=1, args=(target_column, merge_column_left, merge_column_right, prefix, separator, ), meta=dataframe)
    return result_frame



def merge_values(row, target_column, left_column_index, right_column_index, prefix, separator):

    row[target_column] = f"{ prefix }{ row[left_column_index] }{ separator }{ row[right_column_index] }"
    return row
