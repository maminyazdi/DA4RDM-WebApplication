import json
import pandas as pd


def check_conformance(result_dataframe, operation_seq_set1, operation_seq_set2, kpi):
    unique_session_id = pd.unique(result_dataframe.SessionIdCalculated)  # Fetch unique session Ids
    non_conforming_cases = 0
    conforming_cases = 0
    json_op_list = []  # json output
    dataset_start_time = result_dataframe.Timestamp[0]
    dataset_end_time = result_dataframe.Timestamp.iloc[-1]

    for session_id in unique_session_id:
        # Filter result_dataframe based on unique session Ids and store corresponding records in sessionIdFiltered_df
        session_id_filtered_df = result_dataframe[result_dataframe.SessionIdCalculated == session_id]
        # Fetching operations related to session_id
        operation_sequence = list(session_id_filtered_df.Operation)
        # Fetching indices of all records related to session_id
        indices = session_id_filtered_df.index.tolist()

        # Method for checking the sequence of operations in OperationSeqSet1
        non_conforming_cases, conforming_cases = check_op_seq_set1(operation_sequence, indices, operation_sequence,
                                                                   indices, operation_seq_set1, operation_seq_set2,
                                                                   result_dataframe, kpi, json_op_list,
                                                                   non_conforming_cases, conforming_cases)

    total = conforming_cases + non_conforming_cases
    total_json = json.loads(json.dumps(json_op_list))
    print('TOTAL', total_json)
    return total_json, non_conforming_cases, total, dataset_start_time, dataset_end_time

# Method for Eventually Followed By scenario
def conformance_eventually_followed_by(dataframe, op_list1, op_list2, kpi):
    json_op_list = []
    non_conforming_cases = 0
    conforming_cases = 0
    unique_session_id = pd.unique(dataframe.SessionIdCalculated)
    dataset_start_time = dataframe.Timestamp[0]
    dataset_end_time = dataframe.Timestamp.iloc[-1]
    for session_id in unique_session_id:
        # Filter result_dataframe based on unique session Ids and store corresponding records in sessionIdFiltered_df
        session_id_filtered_df = dataframe[dataframe.SessionIdCalculated == session_id]

        # get_operations method for getting all the operations(given in OperationSeqSet1 and OperationSeqSet2) and respective indices from given dataFrame
        operations_oplist1, indices_oplist1 = get_operations(session_id_filtered_df, op_list1)
        operations_oplist2, indices_oplist2 = get_operations(session_id_filtered_df, op_list2)

        # Method for checking the sequence of operations in OperationSeqSet1
        non_conforming_cases, conforming_cases = check_op_seq_set1(operations_oplist1, indices_oplist1,
                                                                  operations_oplist2, indices_oplist2, op_list1,
                                                                  op_list2, dataframe, kpi, json_op_list,
                                                                  non_conforming_cases, conforming_cases)
    total = conforming_cases + non_conforming_cases

    return json_op_list, non_conforming_cases, total, dataset_start_time, dataset_end_time


def get_operations(session_id_filtered_df, op_list):
    indices = session_id_filtered_df.index.tolist()
    index = indices[0]
    operation_sequence = list(session_id_filtered_df.Operation)
    operations_list = []
    indices_list = []
    print('opLen', index, index + len(operation_sequence))
    for i in range(index, index + len(operation_sequence)):
        for j in range(len(op_list)):
            if operation_sequence[i - index] == op_list[j]:
                operations_list.append(operation_sequence[i - index])
                indices_list.append(i)
                break
    return operations_list, indices_list


def check_op_seq_set1(operations_oplist1, indices_oplist1, operations_oplist2, indices_oplist2, op_list1, op_list2, dataframe, kpi, json_op_list, non_conforming_cases, conforming_cases):
    for k in range(len(operations_oplist1) - 1):
        if operations_oplist1[k:k+len(op_list1)] == op_list1:
            print('Inside If df1', indices_oplist1[k:k+len(op_list1)])
            # After checking operationSeqSet1, calling method check_opSeqSet2 to check for operationSeqSet2
            non_conforming_cases, conforming_cases = check_op_seq_set2(indices_oplist1, operations_oplist2,
                                                                      indices_oplist2, dataframe, op_list1, op_list2, k,
                                                                      kpi, json_op_list, non_conforming_cases,
                                                                      conforming_cases)

    return non_conforming_cases, conforming_cases


def check_op_seq_set2(indices_oplist1, operations_oplist2, indices_oplist2, dataframe, op_list1, op_list2, current_index,
                    kpi, json_op_list, non_conforming_cases, conforming_cases):

    print('Inside check_opSeqSet2', indices_oplist1[current_index + len(op_list1) - 1])
    count = 0
    length1 = len(op_list1)
    length2 = len(op_list2)
    for j in range(len(operations_oplist2)):
        combi_list = [] # list which includes last operation of op_list1 and first operation of op_list2
        if indices_oplist2[j] > indices_oplist1[current_index + length1 - 1]:
            print('operation2', operations_oplist2[j:len(operations_oplist2)], indices_oplist2[j:len(indices_oplist2)])
            combi_list.append(indices_oplist1[current_index + length1 - 1])
            combi_list.append(indices_oplist2[j])
            # Performance check between 2 Operation Sequence Sets
            if (kpi != 0) and (kpi != ''):
                non_conforming_cases = time_difference(combi_list, dataframe, kpi, json_op_list, non_conforming_cases)
            for q in range(length2):
                if (j + q) <= len(operations_oplist2):  # Added to avoid out of index error
                    # Added to include last operation of the operation list ,corresponding SessionId
                    operation_index = -1 if j+q >= len(operations_oplist2) else j + q
                    print('Inside new 2nd for', operation_index, operations_oplist2[operation_index], op_list2[q], indices_oplist2[operation_index], j + q, q)
                    if operations_oplist2[operation_index] != op_list2[q]:
                        op_df = dataframe.iloc[indices_oplist2[operation_index]]
                        convert_to_json(op_df, json_op_list)
                        non_conforming_cases = non_conforming_cases + 1
                        break
                    else:
                        count = count + 1
                        if count == length2:
                            conforming_cases = conforming_cases + 1
            break
    return non_conforming_cases, conforming_cases


def time_difference(seq_list, dataframe, kpi, json_op_list, non_conforming_cases):
    i = 0
    while (i < (len(seq_list)-1)):
        time1 = pd.to_datetime(dataframe.Timestamp.iloc[seq_list[i]])
        time2 = pd.to_datetime(dataframe.Timestamp.iloc[seq_list[i+1]])
        print('times', time1, time2)
        time_diff = time2-time1
        total_sec1 = time_diff.total_seconds()
        print('total_sec', total_sec1)
        if total_sec1 > kpi:
            output = dataframe.iloc[seq_list[i+1]]
            convert_to_json(output, json_op_list)
            non_conforming_cases = non_conforming_cases + 1
            print('noOfNonConformance1', non_conforming_cases)

        i = i+1
    return non_conforming_cases


def convert_to_json(output_dataframe, json_op_list):
    json_op = output_dataframe.to_json()  # Converting Pandas dataframe to json string
    json_to_dict = json.loads(json_op)
    json_op_list.append(json_to_dict)  # Converting json string into dictionary
    return


# Adds ProjectId where, ProjectId is null in case of Non-conforming case
def set_project_id(first_index, next_index, current_index, op_seq_set, dataframe):
    if (str(dataframe.ProjectId.iloc[next_index + current_index])) == 'nan':
        # print('Projects',dataFrame.ProjectId.iloc[next_index + current_index - 1])
        project_id = dataframe.ProjectId.iloc[first_index:next_index + len(op_seq_set)].unique()[0]
        # project_id = dataFrame.ProjectId.iloc[next_index + current_index - 1]
        dataframe.ProjectId.iloc[next_index + current_index] = project_id
        print('NewProjectId', dataframe.ProjectId.iloc[next_index + current_index])
    else:
        project_id = dataframe.ProjectId.iloc[next_index + current_index]
    return
