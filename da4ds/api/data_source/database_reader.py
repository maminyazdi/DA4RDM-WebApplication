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

    # specifying the index column can make the data frame creation less taxing in terms of used resources, but is not required. An id column must be unique.
    index_column_name = None
    try:
        index_column_name = parameter_parser.get_parameter(parameter_list, "index_column")
    except Exception:
        print("No index column specified")
        index_column_name = None

    engine = sqlalchemy.create_engine(connection_string)

    with engine.connect() as connection:
        if index_column_name != None:
            try:
                dataframe = pd.read_sql(query, con=engine, index_col=index_column_name)
            except KeyError as err:
                dataframe = pd.read_sql(query, con=engine)
                print(f"Defaulting to creation of data frame without specified id column. Trying to set id column resulted in the following error: {err.args[0]}")
        else:
            dataframe = pd.read_sql(query, con=engine)

        return dataframe

    raise RuntimeError("Error creating a dataframe from the database")