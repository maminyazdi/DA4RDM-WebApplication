from . import sample_project

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
    return config


def run(config):
    """Run the pipeline.
    Expects a configuration"""
    if config._local_database == None:
        #emit('progressLog', {'message': "No Connection to local data base given."})
        print("No Connection to local data base given!")
        return
    else:
        #emit('progressLog', {'message': f"Starting pipepline for { config.PROJECT_NAME }"})
        print(f"Starting pipepline for { config.PROJECT_NAME }")
        #run_steps(config)
        return sample_project.run(config)
