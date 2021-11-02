import json
import pandas as pd

def check_comformance(result_dataframe, operationSeqSet1, operationSeqSet2, KPI):
    unique_session_id = pd.unique(result_dataframe.SessionIdCalculated)     #Fetch unique session Ids
    noOfNonConformance = 0
    noOfConformingCases = 0
    json_op_list = []  #json output
    dataSet_start_time = result_dataframe.Timestamp[0]
    dataSet_end_time = (result_dataframe.Timestamp).iloc[-1]
    print('Timestamp',type(dataSet_start_time),dataSet_start_time,dataSet_end_time)
    for session_id in unique_session_id:
        sessionIdFiltered_df = result_dataframe[result_dataframe.SessionIdCalculated == session_id]   #Filter result_dataframe based on unique session Ids and store corresponding records in sessionIdFiltered_df
        operationSequence = list(sessionIdFiltered_df.Operation) #Fetching operations related to session_id
        temp_seq = operationSequence        # Temporary copy of all Operations related to corresponding session_id
        for i in range(len(operationSequence)):   # Iterating over all operations corresponding to session Id
            if (operationSeqSet1[0] == operationSequence[i]):
                first_index = i             # first_index stores the first index at which operationSeqSet1[0] is found
                print('Before 2nd if', temp_seq[first_index:first_index + len(operationSeqSet1)])
                if (temp_seq[first_index:first_index + len(operationSeqSet1)] == operationSeqSet1):  # comparing with Operation Sequence Set1
                    next_index = first_index + len(operationSeqSet1)        # next_index is equal to the 1st index of operationSeqSet2
                    print('next_seq', temp_seq[next_index:next_index + len(operationSeqSet2)])
                    if ((KPI != 0) and (KPI != '')):     # Performance index check
                        operationSeq_df = sessionIdFiltered_df.iloc[first_index:next_index + len(operationSeqSet2)]
                        if not operationSeq_df[operationSeq_df.Operation == operationSeqSet1[-1]].Timestamp.empty and not operationSeq_df[operationSeq_df.Operation == operationSeqSet2[0]].Timestamp.empty:
                            time1 = (pd.to_datetime(operationSeq_df[operationSeq_df.Operation == operationSeqSet1[-1]].Timestamp.iloc[0]))
                            time2 = (pd.to_datetime(operationSeq_df[operationSeq_df.Operation == operationSeqSet2[0]].Timestamp.iloc[0]))
                            time_diff = time2 - time1
                            total_sec = time_diff.total_seconds()
                            print('total_sec', total_sec)
                            if (total_sec > KPI):       # If total_sec > KPI , then the current operation is non-conforming
                                output = sessionIdFiltered_df.iloc[next_index, :]       # Fetching the Operation for which non-conformance occured
                                json_op = output.to_json()                              # Converting Pandas dataframe to json string
                                jsonToDict = json.loads(json_op)                        # Converting json string into dictionary
                                json_op_list.append(jsonToDict)
                                print('jsonToDict', jsonToDict, type(jsonToDict))
                                noOfNonConformance = noOfNonConformance + 1
                                print('noOfNonConformance1', noOfNonConformance)
                    count = 0
                    # Checking for conformance with operationSeqSet2
                    for i in range(len(operationSeqSet2)):
                        if ((next_index + len(operationSeqSet2)- 1) < len(temp_seq)):            # Condition added to remove out of bound indexing problem
                            if (temp_seq[next_index + i] != operationSeqSet2[i]):       # Checking for each consecutive operations, if not satisfied with the user given operationSeq, then non-conforming case
                                print('not', temp_seq[next_index + i], next_index + i)
                                set_projectId(first_index, next_index, i, operationSeqSet2, sessionIdFiltered_df)    # Method to add ProjectId if empty
                                op_df = sessionIdFiltered_df.iloc[next_index + i, :]
                                op_json = op_df.to_json()
                                opToDict = json.loads(op_json)
                                json_op_list.append(opToDict)
                                noOfNonConformance = noOfNonConformance + 1
                                print('noOfNonConformance', noOfNonConformance)
                                break
                            else:
                                count += 1
                                # count for going through all the operations in OPerationSeqSet2 ...if count == len(operationSeqSet2) , then its a Conforming case
                                if count == len(operationSeqSet2):
                                    noOfConformingCases = noOfConformingCases + 1
                                continue
    total = noOfConformingCases + noOfNonConformance
    total_json = json.loads(json.dumps(json_op_list))
    print('TOTAL', total_json)
    return total_json,noOfNonConformance,total,dataSet_start_time,dataSet_end_time


# Adds ProjectId where, ProjectId is null in case of Non-conforming case
def set_projectId(first_index, next_index, current_index, OpSeqSet, dataFrame):
    if (str(dataFrame.ProjectId.iloc[next_index + current_index])) == 'nan':
        #print('Projects',dataFrame.ProjectId.iloc[next_index + current_index - 1])
        project_id = dataFrame.ProjectId.iloc[first_index:next_index + len(OpSeqSet)].unique()[0]
        #project_id = dataFrame.ProjectId.iloc[next_index + current_index - 1]
        dataFrame.ProjectId.iloc[next_index + current_index] = project_id
        print('NewProjectId', dataFrame.ProjectId.iloc[next_index + current_index])
    else:
        project_id = dataFrame.ProjectId.iloc[next_index + current_index]
    return


