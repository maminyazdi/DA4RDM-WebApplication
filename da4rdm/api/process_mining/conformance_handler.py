import json
import numpy as np

def check_comformance(result_dataframe):
    """"""
    import pandas as pd
    KPI = 60
    unique_session_id = pd.unique(result_dataframe.SessionIdCalculated)
    # df = result_dataframe.groupby('SessionIdCalculated')
    unique_actions = (result_dataframe.Operation).unique()
    print('unique_action',unique_actions)
    prev_action_seq1 = ['View Project', 'Project Create', 'Add Project']
    next_action_seq1 = ['Open Project', 'Project', 'View Project']
    prev_action_seq2 = ['View Project', 'Resource Create', 'Add Resource']
    action1 = 'View Project'
    action2 = 'Open Project'
    #output = pd.DataFrame()
    for sess_id in unique_session_id:
        df1 = result_dataframe[result_dataframe.SessionIdCalculated == sess_id]
        output_dataframe = df1[['ProjectId', 'UserId', 'ResourceId', 'SessionIdCalculated', 'Operation','Timestamp']]
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
                    count=0
                    for i in range(len(next_action_seq1)):
                        print('temp_seq[next_index+i]',temp_seq[next_index+i])
                        print('next_action_seq1[i]',next_action_seq1[i])
                        if (temp_seq[next_index+i] != next_action_seq1[i]):
                            print('not', temp_seq[next_index + i], next_index + i)
                            output = np.ndarray.tolist(df1.iloc[next_index + i, :].values)
                            json_op = json.dumps(output)
                            print('type', type(output))
                            print('type1', type(json_op))
                            print('df1col', df1.columns)
                            print('output', output)
                            print('json_op', json_op)
                            break
                        else:
                            print('nx', temp_seq[next_index + i], next_index + i)
                            count = count+1
                            print('count',count)
                            if count == len(next_action_seq1):
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
                                    op = json.dumps(np.ndarray.tolist(df2[df2.Operation == action2].iloc[0].values)) if(total_sec > KPI) else 0
                                    print('oput',op)


                            continue


                            #op_json = pd.output.to_json()
                            #output1 = pd.DataFrame(df1.iloc[next_index + i : next_index + i + 1, :].values, columns=df1.columns,index=0)

                            #print('op_json', op_json)
                            #print('op_json', type(op_json))

                #print('output1',output)

                            #timestamp1 = pd.to_datetime(df1.iloc[next_index - 1:next_index,2].values)#(df1.iloc[next_index - 1:next_index,2].values).
                            #timestamp2 = pd.to_datetime(df1.iloc[next_index - 1:next_index,2].values)
                            #time_diff = timestamp2.strftime("%S") - timestamp1.strftime("%S")

                            #print('timestamps',type(timestamp1),timestamp2)
                            #print('tp',type(time_diff))
                            #print('Conformance Yes')
                '''else:
                    print()
                    output = output_dataframe.iloc[first_index:first_index + len(prev_action_seq1), :].values
                    #print('output', output)
                    print('Conformance No')

                    # print('output_dataframe',output_dataframe)'''

    return