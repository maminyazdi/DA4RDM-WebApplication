from pm4py.algo.filtering.log.timestamp import timestamp_filter
from pm4py.algo.filtering.log.start_activities import start_activities_filter
from pm4py.algo.filtering.log.end_activities import end_activities_filter
from pm4py.algo.filtering.log.cases import case_filter

def apply_all_filters(event_log, filters):
    """Applies all filters and returns the processed event log."""
    # TODO might need to check for string value "None" as well

    if (filters["process_discovery_start_date"] and filters["process_discovery_end_date"]):
        event_log = apply_timestamp_filter(event_log, filters["process_discovery_start_date"], filters["process_discovery_end_date"])
    elif filters["process_discovery_start_date"]:
        event_log = apply_timestamp_filter(event_log, process_discovery_start_date = filters["process_discovery_start_date"])
    elif filters["process_discovery_end_date"]:
        event_log = apply_timestamp_filter(event_log, process_discovery_end_date = filters["process_discovery_end_date"])

    if (filters["process_discovery_start_activity"] != '[]' and filters["process_discovery_start_activity"] != "['None']"):
        event_log = apply_start_activitiy_filter(event_log, filters["process_discovery_start_activity"])
    if (filters["process_discovery_end_activity"] != '[]' and filters["process_discovery_end_activity"] != "['None']"):
        event_log = apply_end_activitiy_filter(event_log, filters["process_discovery_end_activity"])

    if (filters["process_discovery_min_performance"] and filters["process_discovery_max_performance"]):
        event_log = apply_performance_filter(event_log, filters["process_discovery_min_performance"], filters["process_discovery_max_performance"])

    return event_log


    return """Not yet implemented!"""

def apply_timestamp_filter(event_log, process_discovery_start_date = "0000-01-01 00:00:00", process_discovery_end_date = "2999-12-31 23:59:59", aggregation_method = "traces_combined"):
    """Applies timestamp filters.
    Parameters:
        event_log: pm4py event log
        process_discovery_start_date: string, default = "0000-01-01 00:00:00"
        process_discovery_end_date: string, default = "2999-12-31 23:59:59",
        aggregation_method = "traces_combined"
    return: pm4py event log
    """

    if aggregation_method == "traces_combined":
        filtered_log = timestamp_filter.filter_traces_contained(event_log, process_discovery_start_date, process_discovery_end_date)

    if aggregation_method == "traces_intersecting":
        filtered_log = timestamp_filter.filter_traces_intersecting(event_log, process_discovery_start_date, process_discovery_end_date)

    if aggregation_method == "events":
        filtered_log = timestamp_filter.apply_events(event_log, process_discovery_start_date, process_discovery_end_date)

    return filtered_log

def apply_start_activitiy_filter(event_log, start_activities):
    """"""

    log_start = start_activities_filter.get_start_activities(event_log)
    filtered_log = start_activities_filter.apply(event_log, start_activities)


    return filtered_log

def apply_end_activitiy_filter(event_log, end_activities):
    """"""

    end_activities = end_activities_filter.get_end_activities(event_log)
    filtered_log = end_activities_filter.apply(event_log, end_activities)

    return filtered_log

def apply_performance_filter(event_log, min_performance, max_performance):
    """"""

    filtered_log = case_filter.filter_case_performance(event_log, float(min_performance), float(max_performance))

    return filtered_log

def apply_variants_filter():
    """"""



    return """Not yet implemented!"""
