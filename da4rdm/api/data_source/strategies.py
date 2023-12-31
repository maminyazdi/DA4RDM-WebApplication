def getReadingStrategy(data_source_type, is_stored_on_server):
    """Selects the proper module for generating a dataframe from a variety of datasources."""
    if data_source_type == "csv" and is_stored_on_server: # data source from a csv file on the server
        from . import csv_reader
        return csv_reader
    elif data_source_type == "xes" and is_stored_on_server:
        from . import xes_reader
        return xes_reader
    elif data_source_type == "database" and is_stored_on_server:
        from . import database_reader
        return database_reader
    else:
        raise ImportError("The type of the requested data source could not be handled.")