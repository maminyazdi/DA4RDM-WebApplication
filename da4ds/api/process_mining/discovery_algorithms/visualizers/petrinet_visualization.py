from pm4py.visualization.petrinet import visualizer as pn_visualizer

def visualize(net, initial_marking, final_marking, event_log, variant, output_path):
    parsed_variant = pn_visualizer.Variants.WO_DECORATION
    if variant == 'frequency':
        parsed_variant = pn_visualizer.Variants.FREQUENCY
    if variant == 'performance':
        parsed_variant = pn_visualizer.Variants.PERFORMANCE

    output_format = 'svg'
    parameters = {pn_visualizer.Variants.PERFORMANCE.value.Parameters.FORMAT: output_format}

    gviz = pn_visualizer.apply(net, initial_marking, final_marking, log=event_log, variant=parsed_variant, parameters=parameters)
    pn_visualizer.save(gviz, output_path)