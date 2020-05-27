let session_id = getCurrentSession();
let socket = io.connect('http://' + document.domain + ':' + location.port + '/api/run_process_discovery');

socket.on('updateColumnNames', function(response) {
    resetAllPMOptions();
    updateColumnNames(response);
});

socket.on('ProcessDiscoveryUpdateEverything', function(response) {
    resetAllPMOptions();
    updateEverything(response);
})

socket.emit('requestEventLogPreparation', session_id);


function runProcessDiscovery(hostUrl, projectUrl){
    let hook = document.getElementById('data_target');
    let spinner = document.getElementById('pipeline-running-spinner');

    spinner.style.display="block"
    socket.emit('requestProcessDiscovery', session_id);
    socket.on('progressLog', function(data) {
        hook.textContent = data.message;
    });
    socket.on('gviz', function(response) {
        let img = document.createElement("img");
        spinner.style.display="none";
        img.src = response.replace(/\\/g, "/");
        hook.appendChild(img);
    })

    socket.on('dataframe_information_update', function(response){

    })

    return;
}

function updateEverything(allDiscoveryInformation) {

    updateColumnNames(allDiscoveryInformation["all_column_names"], allDiscoveryInformation["pm_xes_attributes"]);
    updatePMFilters(allDiscoveryInformation["pm_filter_options"], allDiscoveryInformation["pm_filters"]);
    //update other options
    updateKeyMetrics(allDiscoveryInformation["pm_dataframe_key_metrics"])
    return;
}

function resetAllPMOptions() {
    remove_all_options_from_select("timestamp_column");
    remove_all_options_from_select("caseId_column");
    remove_all_options_from_select("activity_column");
    remove_all_options_from_select("resource_column");
    remove_all_options_from_select("cost_column");

    return;
}

function remove_all_options_from_select(elementId) {
    var select = document.getElementById(elementId);
    var length = select.options.length;
    for (i = length-1; i >= 0; i--) {
        select.options[i] = null;
    }
}

function sendXesAttributeColumns() {
    let select_inputs = [document.getElementById("timestamp_column"),
                        document.getElementById("caseId_column"),
                        document.getElementById("activity_column"),
                        document.getElementById("resource_column"),
                        document.getElementById("cost_column")];

    let selectedColumns = {};

    for (let current_select_input of select_inputs) {
        selectedColumns[current_select_input.id] = current_select_input.value;
    }

    socket.emit("requestEventLogPreparation", session_id, selectedColumns);
    return;
}

function sendPMOptions() {
    /*let select_inputs = [document.getElementById("timestamp_column"),
                        document.getElementById("caseId_column"),
                        document.getElementById("activity_column"),
                        document.getElementById("resource_column"),
                        document.getElementById("cost_column")];

    let selectedColumns = {};

    for (let current_select_input of select_inputs) {
        selectedColumns[current_select_input.id] = current_select_input.value;
    }*/
    let selectedXesAttributeColumns = getXesAttributeColumns();
    let selectedPMFilters = getPMFilters();
    let selectedOptions = getDiscoveryOptions();

    socket.emit("requestEventLogPreparation",
                session_id,
                selectedXesAttributeColumns,
                selectedPMFilters,
                selectedOptions);
    return;
}

function updateColumnNames(allColumnNames, selectedColumns) {
    let select_inputs = [document.getElementById("timestamp_column"),
                         document.getElementById("caseId_column"),
                         document.getElementById("activity_column"),
                         document.getElementById("resource_column"),
                         document.getElementById("cost_column")];

    for (let current_select_input of select_inputs) {
        for (let columnName of allColumnNames) {
            var opt = document.createElement('option');
            opt.value = columnName;
            opt.innerHTML = columnName;
            current_select_input.appendChild(opt);
        }
        var opt = document.createElement('option');
        opt.value = "None";
        opt.innerHTML = "None";
        current_select_input.appendChild(opt);

        if (selectedColumns !== undefined && typeof(selectedColumns[current_select_input.id]) !== undefined) {
            current_select_input.value = selectedColumns[current_select_input.id];
        } else {
            current_select_input.value = "None";
        }
    }
}

function updatePMFilters(filterOptions, selectedFilters) {
    startDateSelect = document.getElementById('process_discovery_start_date_select');
    endDateSelect = document.getElementById('process_discovery_end_date_select');
    startActivitySelect = document.getElementById('process_discovery_start_activity');
    endActivitySelect = document.getElementById('process_discovery_end_activity');
    activitySelects = [startActivitySelect, endActivitySelect]
    minPerformanceSelect = document.getElementById('process_discovery_min_performance');
    maxPerformanceSelect = document.getElementById('process_discovery_max_performance');

    startDateSelect.min = filterOptions['timestamp_options']['min'];
    startDateSelect.max = filterOptions['timestamp_options']['max'];
    endDateSelect.min   = filterOptions['timestamp_options']['min'];
    endDateSelect.max   = filterOptions['timestamp_options']['max'];

    for (let activitySelect of activitySelects) {
        for (let activity of filterOptions['activity_options']) {
            var opt = document.createElement('option');
            opt.value = activity;
            opt.innerHTML = activity;
            activitySelect.appendChild(opt);
        }

        var opt = document.createElement('option');
        opt.value = "None";
        opt.innerHTML = "None";
        activitySelect.appendChild(opt);

        if (selectedFilters !== undefined && typeof(selectedFilters[activitySelect.id]) !== undefined) {
            activitySelect.value = selectedFilters[activitySelect.id];
        } else {
            activitySelect.value = "None";
        }
    }

    if (selectedFilters['process_discovery_start_activity'] != undefined) {

    }
    if (selectedFilters['process_discovery_start_activity'] != undefined) {

    }

    minPerformanceSelect.value = (selectedFilters['process_discovery_min_performance'] !== undefined) ? selectedFilters['process_discovery_min_performance'] : '';
    maxPerformanceSelect.value = (selectedFilters['process_discovery_max_performance'] !== undefined) ? selectedFilters['process_discovery_max_performance'] : '';
}

function updateKeyMetrics(metrics) {
    document.getElementById('metrics_number_of_cases').innerHTML      = metrics["number_of_events"];
    document.getElementById('metrics_number_of_events').innerHTML     = metrics["number_of_cases"];
    document.getElementById('metrics_number_of_activities').innerHTML = metrics["number_of_activities"];
    document.getElementById('metrics_number_of_variants').innerHTML   = metrics["number_of_variants"];
}

function getXesAttributeColumns() {
    let select_inputs = [document.getElementById("timestamp_column"),
                         document.getElementById("caseId_column"),
                         document.getElementById("activity_column"),
                         document.getElementById("resource_column"),
                         document.getElementById("cost_column")];

    let selectedColumns = {};

    for (let current_select_input of select_inputs) {
        selectedColumns[current_select_input.id] = current_select_input.value;
    }

    return selectedColumns;
}

function getPMFilters() {
    let select_inputs = [document.getElementById("process_discovery_start_date"),
                         document.getElementById("process_discovery_end_date"),
                         document.getElementById("process_discovery_start_activity"),
                         document.getElementById("process_discovery_end_activity"),
                         document.getElementById("process_discovery_min_performance"),
                         document.getElementById("process_discovery_max_performance")];

    let selectedFilters = {};

    for (let current_select_input of select_inputs) {
        selectedFilters[current_select_input.id] = current_select_input.value;
    }

    return selectedFilters;
}

function getDiscoveryOptions() {
    return undefined;
}

function getColumnNames() {
    socket.emit('requestColumnNames', session_id);
}

function resetAllPMOptions() {
    //reset all ui inputs
    //AND
    //all server side session information on these options!!
}