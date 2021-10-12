import json
import numpy as np
import pandas as pd


def check_comformance(result_dataframe,prev_action_seq1,next_action_seq1,KPI):

    unique_session_id = pd.unique(result_dataframe.SessionIdCalculated)
    unique_count = len(unique_session_id)
    print('uniqueSesscount', unique_count)
    # df = result_dataframe.groupby('SessionIdCalculated')
    #unique_actions = (result_dataframe.Operation).unique()
    #print('unique_action',unique_actions)
    #prev_action_seq1 = ['View Project', 'Project Create', 'Add Project']
    #next_action_seq1 = ['Open Project', 'Project', 'View Project']
    prev_action_seq2 = ['View Project', 'Resource Create', 'Add Resource']
    action1 = prev_action_seq1[-1]
    action2 = next_action_seq1[0]
    noOfNonConformance = 0
    print('KPI',KPI)
    KPI_empty = 0 if KPI == '' else KPI
    print('KPI_empty', KPI_empty)
    #output = pd.DataFrame()
    for sess_id in unique_session_id:
        df1 = result_dataframe[result_dataframe.SessionIdCalculated == sess_id]
        #output_dataframe = df1[['ProjectId', 'UserId', 'ResourceId', 'SessionIdCalculated', 'Operation','Timestamp']]
        print('df1', df1)
        action_seq = list(df1.Operation)
        #df2= df1[df1.Operation == action1].Timestamp
        #df3 = df1[df1.Operation == action2].Timestamp

        '''if not df2.empty and not df3.empty:
            time1 = (pd.to_datetime(df2.iloc[-1]))
            time2 = (pd.to_datetime(df3.iloc[0]))
            print('dftype',type(df2.iloc[-1]),type(df3.iloc[0]))
            print('timetype',type(time1),type(time2))
            print('df2', df2.iloc[-1])
            print('df3', df3)
            print('2', type(df3))
            print('time1', time1)
            print('time2', time2)
            print('type1', type(time1))
            time_diff = time2 - time1
            total_sec = time_diff.total_seconds()
            #time_diff = (time2 - time1) / np.timedelta64(1, 's')
            print('time_diff',total_sec)'''
        #time_diff = (time2 - time1)/np.timedelta64(1,'s') if (time1 is not None & time2 is not None) else print('0')

        temp_seq = action_seq
        for i in range(len(action_seq)):
            if (prev_action_seq1[0] == action_seq[i]):
                # print('Inside if')
                first_index = i
                print('First index',first_index)
                print('Before 2nd if', temp_seq[first_index:first_index + len(prev_action_seq1)])
                #print('Timestamp',df1.iloc[first_index:first_index + len(prev_action_seq1), 2].values)
                if (temp_seq[first_index:first_index + len(prev_action_seq1)] == prev_action_seq1):
                    next_index = first_index + len(prev_action_seq1)
                    print('next_index',next_index)
                    print('next_seq', temp_seq[next_index:next_index + len(next_action_seq1)])

                    if ((KPI != 0) and (KPI != '')):
                        print('Inside KPI_if1')
                        df2 = df1.iloc[first_index:next_index + len(next_action_seq1)]
                        print('df2', df2)
                        df3 = df2[df2.Operation == action1].Timestamp
                        df4 = df2[df2.Operation == action2].Timestamp
                        print('df3', df3)
                        print('df4', df4)
                        if not df3.empty and not df4.empty:
                            time1 = (pd.to_datetime(df2[df2.Operation == action1].Timestamp.iloc[0]))
                            time2 = (pd.to_datetime(df2[df2.Operation == action2].Timestamp.iloc[0]))
                            print('time1', time1)
                            print('time2', time2)
                            time_diff = time2 - time1
                            print('time_diff', time_diff)
                            total_sec = time_diff.total_seconds()
                            # time_diff = (time2 - time1) / np.timedelta64(1, 's')
                            print('total_sec', total_sec)
                            print('KPI_if',(total_sec <= KPI_empty))
                            print('KPI_if', KPI_empty == 0)
                            #print('KPI_if',(total_sec <= KPI)  (KPI_empty == 0))

                            if (total_sec > KPI_empty):
                                print('Inside KPI IF')
                                output2 = np.ndarray.tolist(df1.iloc[next_index, :].values)
                                json_op = json.dumps(output2)
                                noOfNonConformance = noOfNonConformance + 1
                                print('output2', output2)
                                print('json_op', json_op)
                                print('noOfNonConformance1', noOfNonConformance)
                    count = 0
                    for i in range(len(next_action_seq1)):
                        print('temp_seq[next_index+i]', temp_seq[next_index + i])
                        print('next_action_seq1[i]', next_action_seq1[i])
                        if (temp_seq[next_index + i] != next_action_seq1[i]):
                            print('not', temp_seq[next_index + i], next_index + i)
                            # output = np.ndarray.tolist(df1.iloc[next_index + i, :].values)
                            # output1 = np.ndarray.tolist(df1.iloc[next_index, :].values)
                            # json_op = json.dumps(output)
                            session = df1.SessionIdCalculated.iloc[next_index + i]
                            print('sess', df1.SessionIdCalculated.iloc[next_index + i])
                            print('pid', df1[df1.SessionIdCalculated == session].ProjectId.unique())
                            print(str(df1.ProjectId.iloc[next_index + i]))
                            print(type(str(df1.ProjectId.iloc[next_index + i])))
                            print('isnan', (str(df1.ProjectId.iloc[next_index + i])) == 'nan')
                            print('project',df1.ProjectId.iloc[first_index:next_index+len(next_action_seq1)].unique())
                            # project_id = df1[df1.SessionIdCalculated == session].ProjectId.unique() if df1.ProjectId.iloc[
                            # next_index + i] is None else df1.ProjectId.iloc[next_index + i]
                            if (str(df1.ProjectId.iloc[next_index + i])) == 'nan':
                                print('IF1')
                                project_id = df1.ProjectId.iloc[first_index:next_index+len(next_action_seq1)].unique()[0]
                                df1.ProjectId.iloc[next_index + i] = project_id
                                print('NewProjectId', df1.ProjectId.iloc[next_index + i])
                            else:
                                print('ELSE1')
                                project_id = df1.ProjectId.iloc[next_index + i]
                            # df1.ProjectId.iloc[next_index + i] = project_id
                            print('project_id', project_id)
                            op_df = df1.iloc[next_index + i, :]
                            print('op_df', op_df)
                            op_json = op_df.to_json()
                            print('json', op_json)
                            noOfNonConformance = noOfNonConformance + 1
                            # print('type', type(output))
                            # print('type1', type(json_op))
                            # #print('df1col', df1.columns)
                            # print('output', output)
                            # print('json_op', json_op)
                            # print('output1', output1)
                            # print('noOfNonConformance1', noOfNonConformance)
                            break
                        else:
                            count += 1
                            op = 'Conformance Yes' if count == len(next_action_seq1) else count
                            print('op', op)
                            continue
    return