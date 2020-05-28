import re
import pandas as pd
from pm4py.algo.filtering.log.variants import variants_filter

from da4ds.process_mining import ( event_log_generator, filter_handler, mining_handler, visualization_handler, conformance_handler )

def run(session_information):

    event_log = event_log_generator.generate_xes_log(session_information["process_mining_data_location"], separator=';')
    if session_information["pm_filters"]:
        filtered_event_log = filter_handler.apply_all_filters(event_log, session_information["pm_filters"]) # TODO gleiche Auswahl auch für Options machen? Also z.B. Information about Frequency/Perofrmance??
    miner = mining_handler.select_mining_strategy()
    model_type = mining_handler.select_model_type()

    ### temp code
    from pm4py.algo.discovery.dfg import factory as dfg_factory
    dfg = dfg_factory.apply(event_log)

    # this way of vizualizing is outdated?
    #from pm4py.visualization.dfg import factory as dfg_vis_factory
    #gviz = dfg_vis_factory.apply(dfg, log=event_log, variant="frequency")
    from pm4py.visualization.dfg import visualizer as dfg_visualization
    parameters = {dfg_visualization.Variants.PERFORMANCE.value.Parameters.FORMAT: "svg"}
    gviz = dfg_visualization.apply(dfg, log=event_log, variant=dfg_visualization.Variants.FREQUENCY, parameters=parameters)
    #gviz = dfg_visualization.apply(dfg, log=event_log, variant=dfg_visualization.Variants.PERFORMANCE, parameters=parameters)
    output_path = session_information["output_location"] + ".svg"
    dfg_visualization.save(gviz, output_path)

    # TODO # FIXME IMPORTANT the output files are currently not secured in the static folder and can in theory be accessed by anyone connecting to the server!!!
    #session_information["output_location"] = "./da4ds/static/process_mining_output/abc"
    #output_path = session_information["output_location"] + ".png"
    #dfg_vis_factory.save(gviz, output_path)
    output_path_relative = re.sub(r"da4ds/", "", output_path)
    return ['gviz', output_path_relative]

    ###

    vizualization_type = visualization_handler.select_visualization_type()
    conformance_handler.check_comformance()

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