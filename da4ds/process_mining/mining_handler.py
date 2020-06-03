import importlib

def select_mining_strategy(strategy):
    """Returns the proper mining strategy for the selected miner."""

    strategy = importlib.import_module("." + strategy, 'da4ds.process_mining.discovery_algorithms')

    return strategy

def select_model_type():
    """Returns the selected model type"""

    return """Not yet implemented!"""