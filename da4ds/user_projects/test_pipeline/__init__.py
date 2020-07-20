from . import test_pipeline
import pandas as pd

_local_database = None

if __name__ == "__main__":
    pass
else:
    pass

def init(data_source, parameters):
    """Set required values coming from the server and add session information."""
    from .config import Config
    config = Config()
    config.data_source = data_source
    config.parameters = parameters

    #config.data = pd.read_csv("C:/Temp/da4ds_temp1.csv")
    return config


def run(config):
    """Run the pipeline.
    Expects a configuration"""
    print(f"Starting pipepline")
    return test_pipeline.run(config)