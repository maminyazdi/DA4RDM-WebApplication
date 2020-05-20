import numpy as np

def prepare_xes_columns(dataframe, case_column, activity_column, timestamp_column, resource_column, cost_column):
    """ Converts a dataframe into xes viable format for the purpose of processing the data in pm4py.

    Parameters
    ----------

    dataframe: dask.dataframe
        dataframe to work on
    case_column: int or str
        index of the column to become case:concept:name column
    activity_column: int or str
        index of the column to become concept:name column
    timestamp_column: int or str
        index of the column to become time:timestamp column
    resource_column: int or str
        index of the column to become org:resource column
    cost_column: int or str
        index of the column to become org:cost column

    Returns
    -------

    dataframe: dask.dataframe
        new dataframe with the updated values
    """

    # get indeces if only target column names are known
    column_names = dataframe.columns.values.tolist()
    case_column_index      = (case_column)      if (type(case_column)      == 'int') else (column_names.index(case_column))
    activity_column_index  = (activity_column)  if (type(activity_column)  == 'int') else (column_names.index(activity_column))
    timestamp_column_index = (timestamp_column) if (type(timestamp_column) == 'int') else (column_names.index(timestamp_column))
    resource_column_index  = (resource_column)  if (type(resource_column)  == 'int') else (column_names.index(resource_column))
    cost_column_index      = (cost_column)      if (type(cost_column)      == 'int') else (column_names.index(cost_column))

    dataframe = prepare_case_colum(dataframe, case_column_index)
    dataframe = prepare_activity_column(dataframe, activity_column_index)
    dataframe = prepare_timestamp_column(dataframe, timestamp_column_index)
    dataframe = prepare_resource_column(dataframe, resource_column_index)
    # TODO add cost column conversion, check if all the other work as intended

    return dataframe

def prepare_timestamp_column(dataframe, column_index):
    #prepare_head
    column_head = dataframe.columns.values

    if not column_head[column_index].startswith("time:timestamp"):
        column_head[column_index] = "time:timestamp" #+ column_head[column_index]
        dataframe.columns = column_head
        #new_column_name = "time:timestamp" + column_head[column_index]
        #column_head = column_head.insert(column_index, new_column_name)
        #print(column_head)

    print(dataframe.head(20))

    #prepare_values
    #column = dataframe.iloc[:, column_index]

    column_name = column_head[column_index]

    dataframe[column_name] = np.where((not str(dataframe[column_name]).startswith("'time:timestamp':Timestamp('")),"'time:timestamp':Timestamp('" + dataframe[column_name] + "')",dataframe[column_name])
    #dataframe[column_name] = dataframe.applymap(lambda element: element if str(element).startswith("'time:timestamp':Timestamp('") else ("'time:timestamp':Timestamp('" + dataframe[column_name] + "')")) #TODO fing more efficient way

    print(dataframe.shape)

    return dataframe

def prepare_case_colum(dataframe, column_index):
    #prepare_head
    column_head = dataframe.columns.values
    if not column_head[column_index].startswith("case:concept:name"):
        column_head[column_index] = "case:concept:name"# + column_head[column_index]
        dataframe.columns = column_head

    #prepare_values
    column_name = column_head[column_index]
    dataframe[column_name] = np.where((not str(dataframe[column_name]).startswith("'case:concept:name'")),"'case:concept:name': '" + dataframe[column_name] + "'",dataframe[column_name])

    return dataframe

def prepare_activity_column(dataframe, column_index):
    #prepare_head
    column_head = dataframe.columns.values
    if not column_head[column_index].startswith("concept:name"):
        column_head[column_index] = "concept:name"# + column_head[column_index]
        dataframe.columns = column_head

    #prepare_values
    column_name = column_head[column_index]
    dataframe[column_name] = np.where((not str(dataframe[column_name]).startswith("'Activity'")),"'Activity': '" + dataframe[column_name] + "'",dataframe[column_name])

    return dataframe

def prepare_resource_column(dataframe, column_index):
    #prepare_head
    column_head = dataframe.columns.values
    if not column_head[column_index].startswith("org:resource"):
        column_head[column_index] = "org:resource" + column_head[column_index]
        dataframe.columns = column_head

    #prepare_values
    column_name = column_head[column_index]
    dataframe[column_name] = np.where((not str(dataframe[column_name]).startswith("'org:resource'")),"'org:resource': '" + dataframe[column_name] + "'",dataframe[column_name])

    return dataframe
