import pandas as pd
import sqlalchemy

from . import parameter_parser

def generate_dataframe(parameter_list):
    """
    Required parameters:
        connection_string: Connection string that can be parsed by sqlalchemy, including credentials, if required.
        query: Query the data you want to take from the connected database
        index_column_name: Name of the Index column, so that the dataframe uses it properly.
    """

    connection_string = parameter_parser.get_parameter(parameter_list, "connection_string")
    query = parameter_parser.get_parameter(parameter_list, "query")
    index_column_name = parameter_parser.get_parameter(parameter_list, "index_column")

    engine = sqlalchemy.create_engine(connection_string)

    with engine.connect() as connection:
        dataframe = pd.read_sql(query, con=engine, index_col=index_column_name)

        return dataframe

    raise RuntimeError("Error creating a dataframe from the database")