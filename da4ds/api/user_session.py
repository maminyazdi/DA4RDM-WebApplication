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
    new_session.WorkingDataLocation = f'{app.config["TEMP_STORAGE_DIRECTORY"]}{new_session.Id}.csv'
    new_session.OutputDataLocation = f'./da4ds/static/process_mining_output/{new_session.Id}'
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
    session_information['output_location'] = raw_session_information.OutputDataLocation
    session_information['pm_filters'] = parse_pm_filters(raw_session_information.PMFilters)

    return session_information

def update_session(session_id, attribute, value):
    """Tries to parse the given attribute and, if successful, updates the queried user session in the database."""

    session_information = SessionInformation.query.filter_by(Id=session_id).first()
    for att in session_information.__table__.columns:
        print(attribute) # TODO remove debug code
    if attribute in session_information.__table__.columns:
        if attribute == session_information.PMFilters:
            updated_filters = update_filters(session_information, value)
            session_information.PMFilters = updated_filters
        else:
            session.__table__columns[attribute] = value
    db.session.commit()

    return None

def clear_session(session_id):
    """Deletes the queried user session from the data base."""

    session_information = SessionInformation.query.filter_by(Id=session_id).first()
    db.session.delete(session_information)
    db.commit()

    return None

def parse_pm_filters(raw_filters):
    """Extract dictionary of the process mining filter as coming from the session data base object."""

    if raw_filters == None:
        return ""

    filters = {}
    parsed_filters = dict((key.strip(), value.strip()) for key, value in (param.split('=') for param in raw_filters.split(';')))
    for key in parsed_filters:
        if key in ProcessMiningFilters.__dict__:
            filters[key] = parsed_filters[key]

    return filters

def update_filters(session_information, new_filters):
    """f a set of fitler attributes are given,
    they will eb treated as though they are in the same format as the filters stored in the user session table,
    then existing fitler are overwritten while new filters are appended."""

    filters_to_update = parse_pm_filters(session_information.PMFilters)
    new_filters = parse_pm_filters(new_filters)
    for filter in new_filters:
        filters_to_update[filter] = new_filters[filter]

    return filters_to_update