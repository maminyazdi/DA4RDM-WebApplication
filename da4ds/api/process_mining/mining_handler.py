import importlib

def select_mining_strategy(strategy):
    """Returns the proper mining strategy for the selected miner."""

    strategy = importlib.import_module("." + strategy, 'da4ds.api.process_mining.discovery_algorithms')

    return strategy

