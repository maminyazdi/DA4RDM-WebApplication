import pandas as pd
from . import parameter_parser

def generate_dataframe(parameter_list, sep=";"):
    path = parameter_parser.get_parameter(parameter_list, "path")
    try:
        sep = parameter_parser.get_parameter(parameter_list, "separator")
    except Exception:
        pass
    dataframe = pd.read_csv(path, sep=sep);

    return dataframe