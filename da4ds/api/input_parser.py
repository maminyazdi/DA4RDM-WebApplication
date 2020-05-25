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