import pandas as pd
from pm4py.objects.log.importer.xes import importer
from pm4py.objects.conversion.log import converter as log_converter

from . import parameter_parser

def generate_dataframe(parameter_list):
    path = parameter_parser.get_parameter(parameter_list, "path")
    log = importer.apply(path)

    dataframe = log_converter.apply(log, variant = log_converter.Variants.TO_DATA_FRAME)

    return dataframe