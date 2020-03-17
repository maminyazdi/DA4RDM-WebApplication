from da4ds.process_mining import ( event_log_generator, filter_handler, mining_handler, visualization_handler, conformance_handler )

def run():
    dataframe = "Data Frame"
    event_log = event_log_generator.generate_xes_log(dataframe)
    event_log = filter_handler.apply_all_filters() # TODO gleiche Auswahl auch für Options machen? Also z.B. Information about Frequency/Perofrmance??
    miner = mining_handler.select_mining_strategy()
    model_type = mining_handler.select_model_type()
    vizualization_type = visualization_handler.select_visualization_type()
    conformance_handler.check_comformance()

    #TODO everything
    import pandas as pd
    import os
    import re
    from pm4py.objects.log.adapters.pandas import csv_import_adapter
    from pm4py.objects.conversion.log import factory as conversion_factory

    # from pm4py.algo.filtering.pandas.timestamp import timestamp_filter
    # df_timest_events = timestamp_filter.apply_events(dataframe, "2020-01-01 00:00:00", "2020-02-02 23:59:59")
    # log = conversion_factory.apply(dataframe)

    # from pm4py.algo.discovery.dfg import factory as dfg_factory
    # dfg = dfg_factory.apply(log)

    # from pm4py.visualization.dfg import factory as dfg_vis_factory
    # gviz = dfg_vis_factory.apply(dfg, log=log, variant="frequency")

    # api_file_path = os.path.abspath(os.path.dirname(__file__))
    # #pattern = re.compile(r"api[/\\\\]+$")
    # #path = pattern.sub("static\\images\\est.gv.png", api_file_path)
    # path = api_file_path.replace("api", "static\\images\\test.gv.png") # TODO replace static file path
    # dfg_vis_factory.save(gviz, path)
    # emit('gviz', "../static/images/test.gv.png") # TODO replace static file path
    # #dfg_vis_factory.view(gviz)

    # #emit('gviz', dfg_vis_factory.view(gviz))
    # #####

    return #gviz
