from flask_socketio import emit

from da4rdm.processing_libraries.da4rdm import rename_column_labels

def execute(dataframe, column_name, new_column_name, split_target):
    """Split a column of a dataframe into new columns."""

    emit('progressLog', {'message': "Splitting columns."})

    split_columns = dataframe[column_name].str.split(split_target).compute()

    split_column = split_columns.apply(lambda x: '' if len(x) <= 1 else x[1])
    updated_df = dataframe.assign(new_column=split_column) # might have to compute/persist the dataframe in between

    updated_df = rename_column_labels.execute(updated_df, {'new_column': new_column_name})

    return updated_df
