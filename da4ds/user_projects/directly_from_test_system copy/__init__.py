from . import directly_from_test_system
import pandas as pd

_local_database = None

if __name__ == "__main__":
    pass
else:
    pass

def init(session_information, database):
    """Set required values coming from the server and add session information."""
    from .config import Config
    config = Config()
    config._local_database = database
    config.current_session = session_information

    #config.data = pd.read_csv("C:/Temp/da4ds_temp1.csv")
    return config


def run(config):
    """Run the pipeline.
    Expects a configuration"""
    if config._local_database == None:
        print("No Connection to local data base given!")
        return
    else:
        print(f"Starting pipepline")
        return directly_from_test_system.run(config)
