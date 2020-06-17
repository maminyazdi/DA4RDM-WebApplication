from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.visualization.process_tree import visualizer as pt_visualizer
from da4ds.api.process_mining.discovery_algorithms.visualizers import petrinet_visualization

def run(event_log, options, output_path):
    ## petri net
    net, initial_marking, final_marking = inductive_miner.apply(event_log)

    petrinet_visualization.visualize(net, initial_marking, final_marking, event_log, options['model_variant'], output_path)

    ## or tree

    tree = inductive_miner.apply_tree(event_log)
    gviz = pt_visualizer.apply(tree)

    return gviz