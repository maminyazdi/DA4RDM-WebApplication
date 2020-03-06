def getReadingStrategy(data_source_type, is_stored_on_server):
    if data_source_type is "CSV":
        from . import csv_reader
        return csv_reader
    else:
        raise ImportError("The type of the requested data source could not be handled.")