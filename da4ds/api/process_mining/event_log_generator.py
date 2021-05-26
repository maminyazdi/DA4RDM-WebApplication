import pandas as pd
# from da4ds.processing_libraries.da4ds import ( replace_column_values, export_csv, rename_column_labels, split_column, add_column, merge_columns, remove_rows )
# from pm4py.objects.log.adapters.pandas import csv_import_adapter
# from pm4py.objects.conversion.log import factory as conversion_factory

from da4ds.api.process_mining import xes_formatter

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
    from pm4py.objects.log.util import dataframe_utils
    from pm4py.objects.conversion.log import converter as log_converter

    log_csv = pd.read_csv(file_path, sep=separator)

    log_csv['time:timestamp'] = pd.to_datetime(log_csv['time:timestamp'])

    log_csv = log_csv.sort_values('time:timestamp')

    event_log = log_converter.apply(log_csv)

    return event_log