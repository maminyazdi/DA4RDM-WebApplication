import re
import pandas as pd
from flask_socketio import emit
from pm4py.algo.filtering.log.variants import variants_filter

from da4rdm.api.process_mining import (event_log_generator, filter_handler, mining_handler, conformance_handler)

def run(session_information, options):
    #TODO the generation of the model and its visualization might take longer than the ping period of the socket connection. The values for the ping intervall and timeout can be configuredin the main server config.
    # Long-term it might be more sensible to find a more sustainable solution, like having a separate worker thread while the main thread still keeps responding to pings. I tried it briefly but did  not get it to work.
    # Alternatively, a normal HTTP request might be preferred.

    #emit('info', {'message': 'Preparing event log...'})
    event_log = event_log_generator.generate_xes_log(session_information["process_mining_data_location"], separator=';')
    if session_information["pm_filters"]:
        filtered_event_log = filter_handler.apply_all_filters(event_log, session_information["pm_filters"]) # TODO gleiche Auswahl auch für Options machen? Also z.B. Information about Frequency/Perofrmance??
    miner = mining_handler.select_mining_strategy(options['discovery_algorithm'])
    output_path = session_information["output_location"] + "." + options["model_represenations"]
    #emit('info', {'message': 'Starting Discovery...'})
    gviz = miner.run(event_log, options, output_path)

    output_path_relative = re.sub(r"da4rdm/", "", output_path)
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