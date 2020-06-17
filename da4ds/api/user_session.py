import os
from flask import current_app as app
from da4ds.models import SessionInformation
from da4ds.api.process_mining.filters import ProcessMiningFilters
from da4ds.api import input_parser
from da4ds import db
import uuid

parameter_separator = ";"
parameter_type_value_separator = "="

def create_new_session():
    """Generates a new user session using a pseudo-random session id and working data location from the specified configuration paths, stores the session in the database and then returns the session id."""
    #TODO: FIXME: this uuid is potentially not safe, actual permission controll is required
    session_id = str(uuid.uuid4())
    new_session = SessionInformation()
    new_session.Id = session_id

    temp_storage_directory = app.config["TEMP_STORAGE_DIRECTORY"]
    if not temp_storage_directory[-1] == "/":
        temp_storage_directory = temp_storage_directory + "/"

    # FIXME TODO these locations don't need to be in the database as they never change
    # so could have an attribute or a get method only depending on session id
    new_session.UnmodifiedDataLocation = f'{temp_storage_directory}{new_session.Id}/data_cleaning_unmodified_data.csv'
    new_session.WorkingDataLocation    = f'{temp_storage_directory}{new_session.Id}/data_cleaning_working_data.csv'
    new_session.PDDataLocation         = f'{temp_storage_directory}{new_session.Id}/process_discovery_working_data.csv'
    new_session.EventLogLocation       = f'{temp_storage_directory}{new_session.Id}/event_log.xes'
    new_session.OutputDataLocation     = f'./da4ds/static/process_mining_output/{new_session.Id}'
    new_session.PMXesAttributes        = ""
    new_session.PMFilter               = ""
    db.session.add(new_session)
    db.session.commit()

    #create folder for working data
    if not os.path.exists(f'{temp_storage_directory}{new_session.Id}/'):
        os.makedirs(f'{temp_storage_directory}{new_session.Id}')

    return session_id


def get_session_information(session_id):
    """Get all information for the secified session. This includes user id, a reference to the temporary working data, process mining parameters..."""
    #TODO replace with proper session handling

    session_information = {}
    raw_session_information = SessionInformation.query.filter_by(Id=session_id).first()
    session_information['unmodified_data_location'] = raw_session_information.UnmodifiedDataLocation
    session_information['data_location'] = raw_session_information.WorkingDataLocation
    session_information['process_mining_data_location'] = raw_session_information.PDDataLocation
    session_information['event_log_location'] = raw_session_information.EventLogLocation
    session_information['output_location'] = raw_session_information.OutputDataLocation
    session_information['pm_xes_attributes'] = parse_parameter_list(raw_session_information.PMXesAttributes)
    session_information['pm_filters'] = parse_parameter_list(raw_session_information.PMFilters)
    session_information['pm_options'] = parse_parameter_list(raw_session_information.PMOptions)

    return session_information

def update_session(session_id, attribute, value):
    """Tries to parse the given attribute and, if successful, updates the queried user session in the database."""

    session_information = SessionInformation.query.filter_by(Id=session_id).first()
    if attribute in session_information.__table__.columns:
        if attribute == "PMFilters":
            updated_filters = update_parameter_list(session_information, parse_parameter_list(session_information.PMFilters), value)
            updated_filters = input_parser.filters_correct_datetimes(updated_filters)
            session_information.PMFilters = serialize_parameter_list_for_db(updated_filters)
        elif attribute == "PMXesAttributes":
            updated_xes_attributes = update_parameter_list(session_information, parse_parameter_list(session_information.PMXesAttributes), value)
            session_information.PMXesAttributes = serialize_parameter_list_for_db(updated_xes_attributes)
        elif attribute == "PMOptions":
            updated_pm_options = update_parameter_list(session_information, parse_parameter_list(session_information.PMOptions), value)
            session_information.PMOptions = serialize_parameter_list_for_db(updated_pm_options)
        else:
            session.__table__columns[attribute] = value
    db.session.commit()

    return None

def clear_session(session_id):
    """Deletes the queried user session from the data base."""

    # TODO maybe release the disc space by deleting all the tepmorary data from the session
    # or write a job that clears old sessions and removes them from the dabase

    session_information = SessionInformation.query.filter_by(Id=session_id).first()
    db.session.delete(session_information)
    db.commit()

    return None

def parse_parameter_list(raw_parameter_list):
    """Extract dictionary of the process mining filter as coming from the session data base object."""
    parameters = {}

    if raw_parameter_list == '' or raw_parameter_list == None:
        return parameters

    parsed_arguments = dict((key.strip(), value.strip()) for key, value in (param.split(parameter_type_value_separator) for param in raw_parameter_list.split(parameter_separator)))
    # for key in parsed_arguments:
    #     parameters[key] = parsed_arguments[key]

    return parsed_arguments

def update_parameter_list(session_information, arguments_to_update, new_arguments):
    """If a set of filter attributes are given,
    they will be treated as though they are in the same format as the filters stored in the user session table,
    then existing filter are overwritten while new filters are appended."""

    # for deleting these attribute values
    if new_arguments == "":
        return ""

    for parameter in new_arguments:
        arguments_to_update[parameter] = new_arguments[parameter]

    return arguments_to_update

def serialize_parameter_list_for_db(parameters):
    """Serializes a parameter list for as string ofr storage in the local database session table. """

    serialized_parameters = ""
    if len(parameters) > 0:
        for parameter in parameters:
            serialized_parameters = f"{serialized_parameters}{parameter}{parameter_type_value_separator}{parameters[parameter]}{parameter_separator}"

    # remove trailing semicolon
    if len(serialized_parameters) > 0:
        serialized_parameters = serialized_parameters[:-1]

    return serialized_parameters
