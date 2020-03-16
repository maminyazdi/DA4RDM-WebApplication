import pandas as pd

def run(config):
    dataframe = config.data

    dataframe = dataframe.replace(to_replace="'time\:timestamp'\:Timestamp\(", value="", regex=True)
    dataframe = dataframe.replace(to_replace="\)", value="", regex=True)
    dataframe = dataframe.replace(to_replace="-[0-9]+-", value="/", regex=True)
    dataframe = dataframe.replace(to_replace="/[0-9]+ ", value=" ", regex=True)
    dataframe["time:timestamp"] = pd.to_datetime(dataframe["time:timestamp"], utc=True)

    dataframe.to_csv("C:/Temp/da4ds_temp1.csv")

    return "not yet implemented!!!"