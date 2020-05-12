from da4ds.processing_libraries.da4ds import ( replace_column_values, export_csv, rename_column_labels, split_column, add_column, merge_columns, remove_rows )
from pm4py.objects.log.adapters.pandas import csv_import_adapter
from pm4py.objects.conversion.log import factory as conversion_factory

def prepare_event_log_dataframe():
    """Applies all Xes Attribute Columns, prepares these columns for xes format conversion, applies filters to these columns if provided."""

    # read data

    # apply xes columns and format conversion

    # apply possible filters

    # return resulting data frame

    return

def generate_xes_log(file_path, separator):       ###dataframe, case_id_col, activity_col, timestamp_col, cost_col):
    dataframe = csv_import_adapter.import_dataframe_from_path(file_path, sep=separator)
    event_log = conversion_factory.apply(dataframe)

    #TODO check the specified column names and values to see if the yhave the required format and adjust if needed

    return event_log