from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.visualization.process_tree import visualizer as pt_visualizer
from da4rdm.api.process_mining.discovery_algorithms.visualizers import petrinet_visualization
from pm4py.algo.conformance.alignments.petri_net import algorithm as alignments
from pm4py.algo.discovery.footprints import algorithm as footprints_discovery
from pm4py.algo.conformance.tokenreplay import algorithm as token_replay
from pm4py.objects.log.importer.xes import importer as xes_importer


def run(event_log, options, output_path):
    ## petri net
    net, initial_marking, final_marking = inductive_miner.apply(event_log)
#    descriptive_log = xes_importer.apply('C:/Workspace/DA4RDM/da4rdm/da4rdm/temporary_results/479674de-30dd-4bc7-97ce-0529d5b00f1b/event_log.xes')
#    aligned_traces = alignments.apply_log(descriptive_log, net, initial_marking, final_marking)
#    print(aligned_traces)

    petrinet_visualization.visualize(net, initial_marking, final_marking, event_log, options['model_variant'], output_path)

    ## or tree

    tree = inductive_miner.apply_tree(event_log)
    gviz = pt_visualizer.apply(tree)

    return gviz

