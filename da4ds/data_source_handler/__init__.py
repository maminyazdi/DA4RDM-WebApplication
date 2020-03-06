from da4ds.models import DataSource
from . import strategies


def read_from_source(data_source):
    reading_strategy = strategies.getReadingStrategy(data_source.Type, data_source.StoredOnServer)

    return "NOT YET IMPLEMENTED"