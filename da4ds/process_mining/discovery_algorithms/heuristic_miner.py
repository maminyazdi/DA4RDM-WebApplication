from pm4py.algo.discovery.heuristics import algorithm as heuristics_miner
from pm4py.visualization.heuristics_net import visualizer as hn_visualizer

def run(event_log, options, output_path):

    heuristic_net = heuristics_miner.apply_heu(event_log, parameters={heuristics_miner.Variants.CLASSIC.value.Parameters.DEPENDENCY_THRESH: 0.99})

    output_format = options['model_represenations']
    parameters = {"<Parameters.FORMAT: 'format'>": output_format}
   # parameters = {hn_visualizer.Variants.PERFORMANCE.value.Parameters.FORMAT: output_format}

    gviz = hn_visualizer.apply(heuristic_net, parameters = parameters)

    hn_visualizer.save(gviz, output_path)
    # TOTO if the models or visualizations turn out to be unusable, it might help to convert the heuristic net into a petri net first and use the patri net for visualization (cf. alpha miner or inductive miner)
    return