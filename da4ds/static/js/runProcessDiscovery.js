let session_id = getCurrentSession();
let socket = io.connect('http://' + document.domain + ':' + location.port + '/api/run_process_discovery');

socket.on('updateColumnNames', function(response) {
    clearEverything();
    updateColumnNames(response);
});

socket.on('ProcessDiscoveryUpdateEverything', function(response) {
    clearEverything();
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
    //update filters
    //update other options
    updateKeyMetrics(allDiscoveryInformation["pm_dataframe_key_metrics"])
    return;
}

function clearEverything() {
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

function updateFilters() {
    return;
}

function sendFilters() {
    return;
}

function sendStartAndEndDate() {
    return;
}

function sendMetaDecisions() {
    return;
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

        if (typeof(selectedColumns[current_select_input.id]) !== "undefined") {
            current_select_input.value = selectedColumns[current_select_input.id];
        }
    }
}

function updateKeyMetrics(metrics) {
    document.getElementById('metrics_number_of_cases').innerHTML      = metrics["number_of_events"];
    document.getElementById('metrics_number_of_events').innerHTML     = metrics["number_of_cases"];
    document.getElementById('metrics_number_of_activities').innerHTML = metrics["number_of_activities"];
    document.getElementById('metrics_number_of_variants').innerHTML   = metrics["number_of_variants"];
}

function getColumnNames() {
    socket.emit('requestColumnNames', session_id);
}