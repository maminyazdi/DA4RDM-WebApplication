from da4ds.processing_libraries.da4ds import ( replace_column_values, export_csv, rename_column_labels, split_column, add_column, merge_columns, remove_rows )
from pm4py.objects.log.adapters.pandas import csv_import_adapter
from pm4py.objects.conversion.log import factory as conversion_factory

from da4ds.process_mining import xes_formatter

def prepare_event_log_dataframe(dataframe, xes_attributes):
    """Applies all Xes Attribute Columns, prepares these columns for xes format conversion,
    applies filters to these columns if provided."""

    # apply xes columns and format conversion
    dataframe = xes_formatter.prepare_xes_columns(dataframe,
                                      xes_attributes["caseId_column"],
                                      xes_attributes["activity_column"],
                                      xes_attributes["timestamp_column"],
                                      xes_attributes["resource_column"],
                                      xes_attributes["cost_column"])

    # apply possible filters

    return dataframe

def generate_xes_log(file_path, separator):       ###dataframe, case_id_col, activity_col, timestamp_col, cost_col):
    """Generates a pm4py library usable event log from fitting csv file."""

    dataframe = csv_import_adapter.import_dataframe_from_path(file_path, sep=separator)
    event_log = conversion_factory.apply(dataframe)

    return event_log