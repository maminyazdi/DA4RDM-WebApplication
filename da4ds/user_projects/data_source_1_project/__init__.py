from . import data_source_1_project
import pandas as pd

_local_database = None

if __name__ == "__main__":
    pass
else:
    pass

def init(database):
    """Set required values coming from the server."""
    from .config import Config
    config = Config()
    config._local_database = database

    config.data = pd.read_csv("C:/Temp/da4ds_temp1.csv")
    return config


def run(config):
    """Run the pipeline.
    Expects a configuration"""
    if config._local_database == None:
        print("No Connection to local data base given!")
        return
    else:
        print(f"Starting pipepline")
        return data_source_1_project.run(config)
