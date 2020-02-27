from flask_socketio import emit

def execute(df, target_file):
    """Exports the data as csv file.
    This method is intended to give server the means to provide a data export in a tangle form for the user.

    Args:
        dataframe (dask.dataframe): The dataframe to be exported.
        target_file (str): Sting representation of the path to which to write the file.

    Return:
        None
    """
    emit('progressLog', {'message': "Exporting as csv."})

    df.to_csv(target_file)