import pandas as pd
import json

def run(config):
    parameters = config.parameters

    dataframe = pd.read_csv(config.data_source, index_col=0, sep=";")
    print('Dataframe',dataframe)
    print('DFcol',dataframe.columns)

    dataframe = parse_message(dataframe)

    dataframe['Timestamp'] = pd.to_datetime(dataframe['Timestamp'], utc=True, format="%Y-%m-%d %H:%M:%S.%f")
    dataframe = dataframe.sort_values(by="Timestamp")
    dataframe.dropna()
    print('dropna dataframe',dataframe)

    session_id_time_threshold = int(parameters["pipeline_parameters"]) if "pipeline_parameters" in parameters else 30 # in minutes
    dataframe = create_session_ids(dataframe, session_id_time_threshold)

    dataframe.Timestamp = dataframe.Timestamp.dt.strftime("%Y-%m-%d %H:%M:%S.%f")
    dataframe.Timestamp = dataframe.Timestamp.str.slice(0, 23)

    return dataframe

def parse_message(dataframe):
    """parses the "message" column from the Log dataframe and returns a dataframe with the columns parsed from the json contents of Message."""
    #some flawed log entries contain an error message instead of the desired log message and should be cleaned (here: removed)
    print('Message',dataframe.Message)
    #print('Message', dataframe.Message.str)
    dataframe = dataframe[~dataframe.Message.str.contains("Executed action method")]
    message_dataframe = pd.io.json.json_normalize(dataframe.Message.apply(json.loads))
    print('message_dataframe',message_dataframe)

    return message_dataframe

def create_session_ids(dataframe, threshold):
    """Creates session ids by first grouping rows by userId, then detects rows belonging to distinct session by checking
    if any two consecutive rows are further apart from each other than threshold minutes"""

    user_ids = dataframe.UserId.unique()
    new_column_index = len(dataframe.columns)
    return_dataframe = pd.DataFrame()
    threshold = threshold if threshold != '' else 30

    #generate dataframes containing all rows of one user id for each user id
    for user_id in user_ids:
        user_dataframe = dataframe.query(f"UserId == '{user_id}'")
        user_dataframe = user_dataframe.sort_values(by="Timestamp")

        time_diff_series = user_dataframe.Timestamp - user_dataframe.Timestamp.shift()
        threashold_check_series = time_diff_series > pd.Timedelta(value=threshold, unit='m')

        session_id_column = (user_dataframe.UserId[threashold_check_series] + user_dataframe.Timestamp[threashold_check_series].dt.strftime("%d-%m-%Y %H:%M:%S"))

        user_dataframe["SessionIdCalculated"] = session_id_column

        user_dataframe.iloc[0, new_column_index] = user_dataframe.iloc[0, 3] + user_dataframe.iloc[0, 2].strftime("%d-%m-%Y %H:%M:%S")

        user_dataframe.SessionIdCalculated = user_dataframe.SessionIdCalculated.ffill()

        return_dataframe = pd.concat([return_dataframe, user_dataframe], axis=0, join='outer', ignore_index=True, keys=None,
                                     levels=None, names=None, verify_integrity=False, copy=True)

    #maybe sort the resultring dataframe again
    dataframe.sort_values(by="Timestamp")
    print('return_dataframe',return_dataframe)
    print('return_dataframe', return_dataframe.columns)
    return return_dataframe
