import datetime
import sqlalchemy
from flask_socketio import emit

def execute(connection_string, query, local_database, table, time_column, how_to_add):
    """copy all new data from the data sources into the local data base
    arguments:
    connection_string: for the data source, should come from the configuration
    query: for querying the data source, should come from the configuration, gets decorated to deliver only new entries

    Args:
        local_database: model representation for the local database, should be provided from the server, the data model should be set up as to support the table/query
        kind: must be specified to make clear which data model class will be used to handle the query results

    Returns:
        dataframe (dataframe)
    """

    emit('progressLog', {'message': "Creating/Updating local database copy."})

    engine = sqlalchemy.create_engine(connection_string)
    with engine.connect() as connection:
        session = local_database.session
        time_column_name = time_column.key
        error_lines = 0
        most_recent_date = None
        decorated_query = query

        if "time" not in query: #TODO find a more robust way to make sure that the query will be well formed even after appending the where clause, some regex might help; this very crude check just serves to make sure that the initial query can fetch the requested date only fromt he specified date onwards
            most_recent_date = get_most_recent_date(local_database, table, time_column)
            decorated_query = get_query_for_recent_entries(query, most_recent_date, time_column_name)

        results = connection.execute(decorated_query) #FIXME this mehtod is likely to duplicate at least one entry as the last most recent data point considered is rounded down to the last second, so if it actuially has some milliseconds stored in the original database it will be considered more recent thatn itself
        try:
            session = how_to_add(session, results, error_lines)
        except:
            print("no (new) values could be found")
        session.commit()

def get_most_recent_date(database, table, time_column):
    """returns the most recent date as string from the specified database and table objects from the ORM"""

    most_recent_entry = database.session.query(table).order_by(time_column.desc()).first()

    if most_recent_entry == None:
        return None

    most_current_time = (most_recent_entry.__dict__[time_column.key]).strftime('%Y-%m-%dT%H:%M:%S.%f')
    most_current_time_string = str(most_current_time)[:-3]
    return most_current_time_string

def get_query_for_recent_entries(basic_query, filter_date, time_column_name):
    """returns the query for getting data from a database more recent than filter_date"""
    decorated_query = "Query decoration failed."

    if filter_date == None:
        print("Query was not modified. Following query will be executed: { basic_query }")
        return basic_query
    if 'WHERE' in basic_query.upper():
        decorated_query = f"{ basic_query } and { time_column_name } > '{ filter_date }'"
    else:
        decorated_query = f"{ basic_query } where { time_column_name } > '{ filter_date }'"
    return decorated_query