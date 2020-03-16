from da4ds.models import DataSource
from . import strategies
import pandas as pd

def read_from_source(data_source):
    """Selects an data source handler based on the input data and uses it to generate a pandas data frame."""
    reading_strategy = strategies.getReadingStrategy(data_source.Type, data_source.StoredOnServer)
    dataframe = reading_strategy.generate_dataframe(data_source.Parameters)

    return dataframe