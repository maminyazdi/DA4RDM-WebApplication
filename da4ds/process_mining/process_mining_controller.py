import re
import pandas as pd

from da4ds.process_mining import ( event_log_generator, filter_handler, mining_handler, visualization_handler, conformance_handler )

def run(session_information):

    event_log = event_log_generator.generate_xes_log(session_information["data_location"], ',')
    filtered_event_log = filter_handler.apply_all_filters(event_log, session_information["pm_filters"]) # TODO gleiche Auswahl auch für Options machen? Also z.B. Information about Frequency/Perofrmance??
    miner = mining_handler.select_mining_strategy()
    model_type = mining_handler.select_model_type()

### temp code
    from pm4py.algo.discovery.dfg import factory as dfg_factory
    dfg = dfg_factory.apply(event_log)

    from pm4py.visualization.dfg import factory as dfg_vis_factory
    gviz = dfg_vis_factory.apply(dfg, log=event_log, variant="frequency")

# TODO # FIXME IMPORTANT the output files are currently not secured in the static folder and can in theory be accessed by anyone connecting to the server!!!
    #session_information["output_location"] = "./da4ds/static/process_mining_output/abc"
    output_path = session_information["output_location"] + ".png"
    dfg_vis_factory.save(gviz, output_path)
    output_path_relative = re.sub(r"da4ds/", "", output_path)
    return ['gviz', output_path_relative]

###

    vizualization_type = visualization_handler.select_visualization_type()
    conformance_handler.check_comformance()

