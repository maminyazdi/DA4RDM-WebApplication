from pm4py.algo.discovery.alpha import algorithm as alpha_miner
from da4rdm.api.process_mining.discovery_algorithms.visualizers import petrinet_visualization

def run(event_log, options, output_path):

    net, initial_marking, final_marking = alpha_miner.apply(event_log)

    petrinet_visualization.visualize(net, initial_marking, final_marking, event_log, options['model_variant'], output_path)

    return