def check_comformance(result_dataframe):
    """"""
    import pandas as pd
    unique_session_id = pd.unique(result_dataframe.SessionIdCalculated)
    # df = result_dataframe.groupby('SessionIdCalculated')
    prev_action_seq1 = ['View Project', 'Project Create', 'Add Project']
    next_action_seq1 = ['Open Project', 'Project', 'View Project']
    prev_action_seq2 = ['View Project', 'Resource Create', 'Add Resource']
    #output = pd.DataFrame()
    for sess_id in unique_session_id:
        df1 = result_dataframe[result_dataframe.SessionIdCalculated == sess_id]
        output_dataframe = df1[['ProjectId', 'UserId', 'ResourceId', 'SessionIdCalculated', 'Operation','Timestamp']]
        print('df1', df1)
        action_seq = list(df1.Operation)
        # print('action_seq',action_seq)
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
                    for i in range(len(next_action_seq1)):
                        print('temp_seq[next_index+i]',temp_seq[next_index+i])
                        print('next_action_seq1[i]',next_action_seq1[i])
                        if (temp_seq[next_index+i] == next_action_seq1[i]):
                            print('nx',temp_seq[next_index+i], next_index+i)
                            continue
                        else:
                            print('not', temp_seq[next_index + i], next_index + i)
                            #output = output.append(df1.iloc[next_index + i,:].values,ignore_index=True)
                            output = df1.iloc[next_index + i, :].values
                            #output1 = pd.DataFrame(df1.iloc[next_index + i : next_index + i + 1, :].values, columns=df1.columns,index=0)
                            print('type',type(output))
                            print('type1', type(df1.columns))
                            print('df1col',df1.columns)
                            print('output', output)
                            break
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