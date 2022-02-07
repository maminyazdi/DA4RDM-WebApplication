from pm4py.algo.discovery.dfg import algorithm as dfg_discovery
from pm4py.visualization.dfg import visualizer as dfg_visualization

def run(event_log, options, output_path):
    print('dfg_eventlog',event_log)
    print('dfg_options', options)
    dfg = dfg_discovery.apply(event_log)
    output_format = options['model_represenations']

    variant = dfg_visualization.Variants.FREQUENCY
    if options['model_variant'] == 'performance':
        variant = dfg_visualization.Variants.PERFORMANCE

    parameters = {variant.value.Parameters.FORMAT: output_format}
    gviz = dfg_visualization.apply(dfg, log=event_log, variant=variant, parameters=parameters)

    dfg_visualization.save(gviz, output_path)

    return
