from . import KPI_analysis

_local_database = None

if __name__ == "__main__":
    pass
else:
    pass



def init(data_source, parameters):
    """Set required values coming from the server and add session information."""
    from config import Config
    config = Config()
    config.data_source = data_source
    print('DataSource',config.data_source)
    config.parameters = parameters
    print('Parameters', config.parameters)

    return config


def run(config):
    """Run the pipeline.
    Expects a configuration"""
    print(f"Starting process_discovery pipepline")
    return KPI_analysis.run(config)
