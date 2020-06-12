import re
import pandas as pd
from pm4py.algo.filtering.log.variants import variants_filter

from da4ds.process_mining import ( event_log_generator, filter_handler, mining_handler, visualization_handler, conformance_handler )

def run(session_information, options):
    event_log = event_log_generator.generate_xes_log(session_information["process_mining_data_location"], separator=';')
    if session_information["pm_filters"]:
        filtered_event_log = filter_handler.apply_all_filters(event_log, session_information["pm_filters"]) # TODO gleiche Auswahl auch für Options machen? Also z.B. Information about Frequency/Perofrmance??
    miner = mining_handler.select_mining_strategy(options['discovery_algorithm'])
    output_path = session_information["output_location"] + "." + options["model_represenations"]
    gviz = miner.run(event_log, options, output_path)
    model_type = mining_handler.select_model_type()

    output_path_relative = re.sub(r"da4ds/", "", output_path)
    return ['gviz', output_path_relative]

def get_dataframe_key_metrics(dataframe, event_log, xes_attribute_columns):
    """Calculates the key dataframe values used to inform about the data set for process discovery."""

    number_of_events     = len(dataframe.index)
    number_of_cases      = len(dataframe['case:concept:name'].unique())
    number_of_activities = len(dataframe['concept:name'].unique())

    key_metrics = {"number_of_events":     number_of_events,
                   "number_of_cases":      number_of_cases,
                   "number_of_activities": number_of_activities,
                   "number_of_variants":   len(variants_filter.get_variants(event_log))}

    return key_metrics