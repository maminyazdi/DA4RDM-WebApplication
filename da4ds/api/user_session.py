from flask import current_app as app
from da4ds.models import SessionInformation
from da4ds.process_mining.filters import ProcessMiningFilters
from da4ds import db
import uuid

def create_new_session():
    """Generates a new user session using a pseudo-random session id and working data location from the specified configuration paths, stores the session in the database and then returns the session id."""
    #TODO: FIXME: this uuid is potentially not safe, actual permission controll is required
    session_id = str(uuid.uuid4())
    new_session = SessionInformation()
    new_session.Id = session_id
    new_session.WorkingDataLocation = f'{app.config["TEMP_STORAGE_DIRECTORY"]}/{new_session.Id}/data_cleaning_working_data.csv'
    new_session.PDDataLocation      = f'{app.config["TEMP_STORAGE_DIRECTORY"]}/{new_session.Id}/process_discovery_working_data.csv'
    new_session.OutputDataLocation  = f'./da4ds/static/process_mining_output/{new_session.Id}'
    new_session.PMXesAttributes = ""
    new_session.PMFilter = ""
    db.session.add(new_session)
    db.session.commit()
    return session_id


def get_session_information(session_id):
    """Get all information for the secified session. This includes user id, a reference to the temporary working data, process mining parameters..."""
    #TODO replace with proper session handling

    session_information = {}
    raw_session_information = SessionInformation.query.filter_by(Id=session_id).first()
    session_information['data_location'] = raw_session_information.WorkingDataLocation
    session_information['process_mining_data_location'] = raw_session_information.PDDataLocation
    session_information['output_location'] = raw_session_information.OutputDataLocation
    session_information['pm_xes_attributes'] = parse_parameter_list(raw_session_information.PMXesAttributes)
    session_information['pm_filters'] = parse_parameter_list(raw_session_information.PMFilters)

    return session_information

def update_session(session_id, attribute, value):
    """Tries to parse the given attribute and, if successful, updates the queried user session in the database."""

    session_information = SessionInformation.query.filter_by(Id=session_id).first()
    if attribute in session_information.__table__.columns:
        if attribute == session_information.PMFilters:
            updated_filters = update_parameter_list(session_information, parse_parameter_list(session_information.PMFilters), value)
            session_information.PMFilters = updated_filters
        elif attribute == session_information.PMXesAttributes:
            updated_xes_attributes = update_parameter_list(session_information, parse_parameter_list(session_information.PMXesAttributes), value)
            session_information.PMXesAttributes = updated_xes_attributes
        else:
            session.__table__columns[attribute] = value
    db.session.commit()

    return None

def clear_session(session_id):
    """Deletes the queried user session from the data base."""

    # TODO maybe release the disc space by deleting all the tepmorary data from the session

    session_information = SessionInformation.query.filter_by(Id=session_id).first()
    db.session.delete(session_information)
    db.commit()

    return None

def parse_parameter_list(raw_parameter_list):
    """Extract dictionary of the process mining filter as coming from the session data base object."""

    if raw_parameter_list == None:
        return ""

    parameters = {}
    parsed_arguments = dict((key.strip(), value.strip()) for key, value in (param.split('=') for param in raw_parameter_list.split(';')))
    for key in parsed_arguments:
        if key in ProcessMiningFilters.__dict__:
            parameters[key] = parsed_arguments[key]

    return parameters

def update_parameter_list(session_information, arguments_to_update, new_arguments):
    """If a set of filter attributes are given,
    they will be treated as though they are in the same format as the filters stored in the user session table,
    then existing filter are overwritten while new filters are appended."""

    arguments_to_update = parse_parameter_list(session_information.PMFilters)
    new_arguments = parse_parameter_list(new_arguments)
    for parameter in new_arguments:
        arguments_to_update[parameter] = new_arguments[parameter]

    return arguments_to_update