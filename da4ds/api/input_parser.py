def parse_parameter_list(raw_parameter_list, parameter_separator, parameter_type_value_separator):
    """Extract dictionary from a formatted string serialization of the parameter list."""
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

    for parameter in new_arguments:
        arguments_to_update[parameter] = new_arguments[parameter]

    return arguments_to_update

def serialize_parameter_list_for_db(parameters, parameter_separator, parameter_type_value_separator):
    """Serializes a parameter list for as string ofr storage in the local database session table. """

    serialized_parameters = ""
    for parameter in parameters:
        serialized_parameters = f"{serialized_parameters}{parameter}{parameter_type_value_separator}{parameters[parameter]}{parameter_separator}"

    # remove trailing semicolon
    if len(serialized_parameters) > 0:
        serialized_parameters = serialized_parameters[:-1]

    return serialized_parameters

def filters_correct_datetimes(filters):
    """Checks and correccts the format of the date time filters inside the filter dictionary.

    Paramter:
        filters: dictionary of filters

    Returns:
        filters: updated dictionary of filters."""

    if filters["process_discovery_start_date"]:
        filters["process_discovery_start_date"] = format_datetime(filters["process_discovery_start_date"])
    if filters["process_discovery_end_date"]:
        filters["process_discovery_end_date"] = format_datetime(filters["process_discovery_end_date"])

    return filters

def format_datetime(datetime):
    """Serializes the incoming date time string and formats it for storage.
    Conforms to the requirements for usage in process discovery with pm4py.

    Params:
        datetime: date time string.
    Return:
        String with date and time in the following format: YYYY/MM/DD hh:mm:ss
        If the automatic detection of the incoming date time string fails, returns the incoming string instead."""

    if datetime == "" or datetime == None:
        return ""
    elif datetime.count("T") == 1:
        formatted_datetime = " ".join(datetime.split('T'))
        return formatted_datetime
    else:
        return datetime
