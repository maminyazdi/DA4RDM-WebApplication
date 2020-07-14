def get_download_path(session, requested_file):
    """"""

    path = ""

    if requested_file == "unmodified_data":
        path = session["unmodified_data_location"].replace('./da4ds/','').replace('/','\\')
    if requested_file == "working_data":
        path = session["data_location"].replace('./da4ds/','').replace('/','\\')
    if requested_file == "process_mining_data":
        path = session["process_mining_data_location"].replace('./da4ds/','').replace('/','\\')
    if requested_file == "event_log":
        path = session["event_log_location"].replace('./da4ds/','').replace('/','\\')
    if requested_file == "output":
        location = session["output_location"] + "." + session["pm_options"]["model_represenations"]
        path = location.replace('./da4ds/','').replace('/','\\')

    return path
