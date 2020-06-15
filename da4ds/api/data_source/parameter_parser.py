def get_parameter(parameter_list, parameter):
    """split the parameter string into a list of strings of each parameter deliniated by ';', then spleat each parameter into a key-value pair deliniated by ':='
    """

    #TODO  mabye use JSON for parameter serialization?

    parameter_dictionary = dict((key.strip(), value.strip()) for key, value in (param.split(':=') for param in parameter_list.split(';')))
    for key in parameter_dictionary:
        if key == parameter:
            return parameter_dictionary[key]
    raise KeyError("The requested parameter was not found in the specified data source.")
