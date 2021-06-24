import dask.dataframe as dd
import numpy as np

from da4rdm.processing_libraries.da4rdm import rename_column_labels

def execute(dataframe, series, new_column_name):
    """Adds a series object as a column to a dataframe."""

    updated_df = dataframe.assign(new_column=series) #(new_column_names[1], np.dtype(str)))) #TODO might have to compute/persist the dataframe in between
    updated_df = rename_column_labels.execute(updated_df, {'new_column': new_column_name})

    return updated_df
