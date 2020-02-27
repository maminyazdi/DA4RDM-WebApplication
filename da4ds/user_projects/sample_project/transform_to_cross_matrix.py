import os
import csv
import pandas as pd
import dask.dataframe as dd
from flask_socketio import emit

from da4ds.processing_libraries.da4ds import (drop_na, drop_duplicates, fill_na)

def execute(backend_df, frontend_df, binary=False):
    """Generates the specific cross matrix required for sample project analysis.
    This is achieved by grouping frontned and backend logs by access tokens. Then each of this groups gets iterated through line wise. Instances of bulks of same subsequent Rids on the backend will form a data point in the transformed matrix. It will contain the count (or dichotomous representation) of all the methods that can be assiciated with it. This assiciation will be established when the Rids on the front and the backend match (for subsequent entries). I.e. This algorithm walks through the frontend logs in order, checks if the Rid matches the backend rid - if there is a match, it walks through the backend logs and adds the methods it encounters to the curresponding method count for this bulk (i.e. activity) until there is no longer a match. Then it goes on to walk through the front end logs again until the access token group is finished. When Rid = 0 is encountered, during this process, a separate activity with the name 'loading' is created and then treated as if it were a frontend activity, even though it is distinct from the front end activity that is currently under scrutiny.
    Example:
        Frontend:                   Backend:
        Method | Rid                Call | Rid
        A      | 1                  abc  | 2
        B      | 2                  def  | 2
        C      | 3                  abc  | 0
        D      | 4                  xyz  | 0
        E      | 5                  abc  | 0
        A      | 1                  qwe  | 4
        B      | 2                  rtz  | 2
        F      | 3                  rtz  | 2
        G      | 4                  abc  | 2

        Will result in:
        activity | abc | def | xyz | qwe | rtz
        B        | 1   | 1   |     |     |
        loading  | 2   |     | 1   |     |
        D        |     |     |     | 1   |
        B        | 1   |     |     |     | 2
    """

    #emit('progressLog', {'message': "Transforming into cross matrix."})

    access_tokens = frontend_df['AccessToken'].unique()
    meta_dict = {}
    group_index = 0

    frontend_column_names = frontend_df.columns.tolist()
    frontend_rid_index = frontend_column_names.index('Rid') + 1
    frontend_activity_index = frontend_column_names.index('Method') + 1
    backend_column_names = backend_df.columns.tolist()
    backend_rid_index = backend_column_names.index('Rid') + 1
    backend_call_index = backend_column_names.index('Call') + 1

    for access_token in access_tokens:

        iterating_0_rids = False
        iterating_frontend = False

        temp_storage_path_frontend = f"./temp/current_frontend/{ access_token }.csv"
        temp_storage_path_backend = f"./temp/current_backend/{ access_token }.csv"

        current_frontend_rows = frontend_df[frontend_df['AccessToken'].eq(access_token)]
        current_backend_rows = backend_df[backend_df['AccessToken'].eq(access_token)]

        current_frontend_rows = fill_na.execute(current_frontend_rows, 'Rid', 'ffill')
        current_frontend_rows = drop_na.execute(current_frontend_rows)
        current_frontend_rows = drop_duplicates.execute(current_frontend_rows)
        if len(current_frontend_rows) == 0:
            continue

        current_backend_rows = fill_na.execute(current_backend_rows, 'Rid', 'ffill')
        current_backend_rows = drop_na.execute(current_backend_rows)
        if len(current_backend_rows) == 0:
            continue

        #emit('progressLog', {'message': f"Transforming into cross matrix: AccessToken: { access_token }."})

        current_frontend_rows.to_csv(temp_storage_path_frontend, single_file=True)
        current_backend_rows.to_csv(temp_storage_path_backend, single_file=True)

        with open(temp_storage_path_frontend) as frontend_file:
            frontend_reader = csv.reader(frontend_file, delimiter=',')
            with open(temp_storage_path_backend) as backend_file:
                backend_reader = csv.reader(backend_file, delimiter=',')

                frontend_row = next(frontend_reader, 'break') # skip the first lines which contain the column names
                frontend_row = next(frontend_reader, 'break')
                backend_row = next(backend_reader, 'break')
                backend_row = next(backend_reader, 'break')
                iterating_0_rids = False
                iterating_frontend = True

                while(frontend_row != 'break' and backend_row != 'break'):
                    activity = frontend_row[frontend_activity_index]
                    backend_call = backend_row[backend_call_index]
                    if backend_row[backend_rid_index] == '0':
                        #if the rid is 0, add the mothods to "loading", then go to next backend row
                        if not iterating_0_rids:
                            group_index += 1
                            iterating_0_rids = True
                            meta_dict[group_index] = {}
                            meta_dict[group_index]['activity'] = 'loading'

                        if backend_call not in meta_dict[group_index]:
                            meta_dict[group_index][backend_call] = 0
                        meta_dict[group_index][backend_call] += 1
                        backend_row = next(backend_reader, 'break')
                    elif frontend_row[frontend_rid_index] == backend_row[backend_rid_index]:
                        #els if rid in both logs are the same, check if you just got a new front end row; if so, add a new activity, else add to previous activity
                        if iterating_frontend or iterating_0_rids:
                            group_index += 1
                            iterating_0_rids = False
                            iterating_frontend = False
                            meta_dict[group_index] = {}
                            meta_dict[group_index]['activity'] = activity

                        if backend_call not in meta_dict[group_index]:
                            meta_dict[group_index][backend_call] = 0
                        meta_dict[group_index][backend_call] += 1
                        backend_row = next(backend_reader, 'break')
                    else:
                        #contunie with next row from front end logs
                        iterating_0_rids = False
                        iterating_frontend = True
                        frontend_row = next(frontend_reader, 'break')


        os.remove(temp_storage_path_frontend)
        os.remove(temp_storage_path_backend)

    cross_matrix = pd.DataFrame(meta_dict).T
    cross_matrix = cross_matrix.fillna(0)

    if binary:
        cross_matrix[cross_matrix >= 1] = 1 # this does not work any more, since the activities are now a normal feature column with type string rather than the index column

    return cross_matrix
