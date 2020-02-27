from da4ds.processing_libraries.da4ds import ( create_local_database_copy, read_local_database, read_csv, replace_column_values, export_csv,
    drop_duplicates, drop_na, rename_column_labels, split_column, add_column, merge_columns, create_json_response, serialize_as_json,
    multiply_rows, remove_rows, fill_na)
from da4ds.models import ( CopiedFrontendLogs, CopiedBackendLogs )
## import datetime

from sklearn.svm import SVC

def run(config):
    dataframes = {}
    #from . import get_source_data
    #dataframes = get_source_data.run(config)
    # get working data

    # time_a=datetime.datetime.now() ## used in the old code below
    # create_local_database_copy.execute(config.SOURCE_CONNECTION_STRING, config.SOURCE_QUERY_FRONTEND, config._local_database, CopiedFrontendLogs, CopiedFrontendLogs.Time, add_frontend_logs)
    # create_local_database_copy.execute(config.SOURCE_CONNECTION_STRING, config.SOURCE_QUERY_BACKEND, config._local_database, CopiedBackendLogs, CopiedBackendLogs.Time, add_backend_logs)

    for kind in config.DATA_SETS:
        #dataframes[kind] = read_local_database.execute(config._local_database, kind)
        dataframes[kind] = read_csv.execute(config.CSV_SOURCE_MAP[kind])

    # backend cleaning
    backend_df = dataframes['backend_logs']
    #backend_df = split_column.execute(backend_df, 'Resource', 'Rid', r'&_rid=')
    #comment in with db date    backend_df = add_column.execute(backend_df, backend_df.Resource, 'Rid') # TODO This must be commented in when working with the life database
    #comment in with db date    backend_df = rename_column_labels.execute(backend_df, {'Resource': 'Call'})
    backend_df = replace_column_values.execute(backend_df, 'Rid', r'.*&_rid=', '')
    backend_df = replace_column_values.execute(backend_df, 'Call', r'\?.*', '')
    backend_df = replace_column_values.execute(backend_df, 'Call', r'.*\/api\/v2', '')
    backend_df = replace_column_values.execute(backend_df, 'Call', r'(?!.*ParseOTA.*)^eScience/PID/[0-9a-zA-Z-/]*', 'eScience/PID/PIDNumber')
    backend_df = replace_column_values.execute(backend_df, 'Call', r'^eScience/Archive/Store/[0-9a-zA-Z-/]*', 'eScience/Archive/Store')
    backend_df = replace_column_values.execute(backend_df, 'Call', r'eScience/Archive/Store.*', 'eScience/Archive/Store')
    backend_df = replace_column_values.execute(backend_df, 'Rid', r'(?=^[^\s]\D+)(.*)', float("NaN"))
    backend_df = drop_duplicates.execute(backend_df)

    #frontend cleaning
    frontend_df = dataframes['frontend_logs']
    frontend_df = rename_column_labels.execute(frontend_df, {'Counter': 'Rid', 'Resource': 'Page'})
    frontend_df = replace_column_values.execute(frontend_df, 'Method', r'.*#', '')
    frontend_df = replace_column_values.execute(frontend_df, 'Page', r'.*#', '')
    frontend_df = replace_column_values.execute(frontend_df, 'Page', r'\?pid=.*', 'PIDNumber')
    frontend_df = replace_column_values.execute(frontend_df, 'Page', r'\?ota=.*', 'OTANumber')
    frontend_df = replace_column_values.execute(frontend_df, 'Page', r'\?pubid=.*', 'publicationsParameters')
    frontend_df = replace_column_values.execute(frontend_df, 'Rid', r'(?=^[^\s]\D+)(.*)', float("NaN"))
    frontend_df = fill_na.execute(frontend_df, 'Rid', 'ffill')
    frontend_df = rename_activities(frontend_df)

    # time_b = datetime.datetime.now()
    # create transformation matrix
    from da4ds.user_projects.sample_project import transform_to_cross_matrix
    cross_matrix = transform_to_cross_matrix.execute(backend_df, frontend_df, False)
    # time_be = datetime.datetime.now()
    #get median count
    grouped = cross_matrix.groupby('activity')
    print(grouped)
    count_grouped = grouped.size()
    print(count_grouped)
    median = count_grouped.median()
    print(median)
    # jetzt noch für jede vorkommende size auf den median skalieren

    # balance the matrix TODO find a way to remove a selected amount of rows from data which occurs too often -> could find all the rows, then rmove them at random
    # this might need to be adjusted after each change in the data set that changes the amount of rows per activity
    # TODO balancing by adding rows should also implement a way to append randomly chosen rows from the set of rows that need to be repeated
    cross_matrix = remove_rows.execute(cross_matrix, 'activity' ,71, 12)
    cross_matrix = multiply_rows.execute(cross_matrix, 'activity', 1, 11)
    cross_matrix = multiply_rows.execute(cross_matrix, 'activity', 2, 5)
    cross_matrix = multiply_rows.execute(cross_matrix, 'activity', 3, 3)
    cross_matrix = multiply_rows.execute(cross_matrix, 'activity', 8, 1)

    print(cross_matrix.groupby('activity').count())

    # cross_matrix.to_csv('C:/Temp/testtest.csv') ## old code need to check if this is needed still

    prediction_goodness = make_prediction(cross_matrix, 'activity')

    # time_ae = datetime.datetime.now() ## old code need to check if this is needed still
    # deltaa= time_ae - time_a
    # deltab = time_be - time_b

    # print(deltaa, deltab)
    return {'name': 'Sample Project', 'kind': 'barCharts', 'data': prediction_goodness, 'options': {'title': 'Metrics', 'subtitle': 'Comparing different metrics for the quality of the prediction.'}}

#TODO find a better way to add access the local and external database columns
def add_frontend_logs(session, data, error_lines): #TODO add correct values, maybe restructure to reduce duplicate code; might also use the __dict__ do dynamically read the attributes if they are the same on both sides
    for datum in data:
        try:
            frontend_log = CopiedFrontendLogs(#Id          = datum.Id,
                                              Time        = datum.Time,
                                              AccessToken = datum.AccessToken,
                                              Resource    = datum.Resource,
                                              Method      = datum.Method,
                                              Counter     = datum.Counter
            )
            session.add(frontend_log)
        except:
            continue
    return session

def add_backend_logs(session, data, error_lines): #TODO add correct values
    for datum in data:
        try:
            backend_log = CopiedBackendLogs(#Id          = datum.Id,
                                            Time        = datum.Time,
                                            AccessToken = datum.AccessToken,
                                            ServiceScope = datum.ServiceScope,
                                            Resource    = datum.Resource
            )
            session.add(backend_log)
        except:
            continue
    return session

def rename_activities(df): # TODO check content wise correctness of renamings
    df = replace_column_values.execute(df, 'Method', r'terms_conditions_confirm\.btn\.btn-primary\.acceptTOSArchiveButton', 'acceptTOSArchiveButton')
    df = replace_column_values.execute(df, 'Method', r'accept-tos\.btn\.btn-primary', 'acceptTermsOfService')
    #df = replace_column_values.execute(df, 'Method', r'restore-tab\.list-group-item\.list-group-item-action\.menu-action', '')
    #df = replace_column_values.execute(df, 'Method', r'manage-tab\.list-group-item\.list-group-item-action\.menu-action', '')
    #df = replace_column_values.execute(df, 'Method', r'select2-http//purlorg/dc/elements/subject-container\.select2-selection__rendered', '')
    df = replace_column_values.execute(df, 'Method', r'save_button\.btn\.btn-primary\.pull-right', 'submitMetadata')
    df = replace_column_values.execute(df, 'Method', r'/html/body/div\[.*]/div\[.*]/div/div\[.*]/main/div/div\[.*]/div/div/form/div\[.*]/div/div/div/div/table/tbody/tr\[.*]/td\.metadata-col-title\.tableEntry\.datatable-title-column', 'clickMetadataRow')
    df = replace_column_values.execute(df, 'Method', r'https://www\.rwth-aachen\.de/metadata/schemas/.*schemaIdBtn\.schemaSelected', 'metadataSchemaSelected')
    df = replace_column_values.execute(df, 'Method', r'uploadButton\.btn\.btn-primary\.disabled', 'uploadDisabled')
    #df = replace_column_values.execute(df, 'Method', r'/div/header/nav/div/ul/li/a/span\.language-box', '')
    #df = replace_column_values.execute(df, 'Method', r'/html/body/div\[2]/div\[6]/div/div\[2]/main/div/div\[3]/div/div\[4]/div/div\[3]/div/div/form/div/div/div\[6]/div/span/span/span/span/span\.select2-selection__placeholder', '')
    #df = replace_column_values.execute(df, 'Method', r'/html/body/div\[2]/div\[6]/div/div\[2]/main/div/div\[4]/div/div\[2]/div/div/div/div/div/table/tbody/tr/td\.metadata-col-title\.tableEntry\.datatable-title-column', '')
    #df = replace_column_values.execute(df, 'Method', r'/div/header/nav/div/ul/li\[2]/a', '')
    df = replace_column_values.execute(df, 'Method', r'delete_confirm\.btn\.btn-secondary\.deleteMetadataButton', 'deleteMetadata')
    df = replace_column_values.execute(df, 'Method', r'schema_rendered', 'schema_rendered')
    df = replace_column_values.execute(df, 'Method', r'button.*btn\.btn-success\.restoreBtn', 'restore')
    df = replace_column_values.execute(df, 'Method', r'/html/body/div\[.*]/div\[.*]/div/div\[.*]/main/div/div\[.*]/div/div/div\[.*]/div/table/tbody/tr\[.*]/td\[.*]/a/i\.material-icons\.col-sm-2\.downloadButton', 'download')
    #df = replace_column_values.execute(df, 'Method', r'/html/body/div[3]/div[6]/div.container', '')
    #df = replace_column_values.execute(df, 'Method', r'metadata_navigation', '')
    #df = replace_column_values.execute(df, 'Method', r'http://purl\.org/dc/terms/abstract\.form-control\.metadata_property', '')
    df = replace_column_values.execute(df, 'Method', r'/div/div\[.*]/div/div/div/div/div/table/tbody/tr/td\[.*]\.metadata-col-visibility', 'orderMetadataByVisibility')

    df = merge_columns.execute(df, 'Page', 'Method', 'Method', '@', '|')

    return df

def make_prediction(cross_matrix, label_column):
    from da4ds.processing_libraries.da4ds import (split_train_test_sets, random_forest_fit, random_forest_predict, check_prediction)
    goodness = []
    metrics = ['Algorithm'] + ['Recall', 'Precision', 'Accuracy', 'F1 Score'] # TODO: let user select the required metrics from config

    goodness += [metrics]

    train_features, test_features, train_labels, test_labels = split_train_test_sets.execute(cross_matrix, label_column, 42)
    random_forest_model = random_forest_fit.execute(train_features, train_labels, 42)
    random_forest_predictions = random_forest_predict.execute(random_forest_model, test_features)
    goodness.append(["Random Forest"] + check_prediction.execute(random_forest_predictions, test_labels, 'macro'))

    svc_classifier = SVC()
    svc_classifier.fit(train_features, train_labels)
    svc_predictions = svc_classifier.predict(test_features)
    goodness.append(["Svm Classification"] + check_prediction.execute(svc_predictions, test_labels, 'macro'))

    return goodness
