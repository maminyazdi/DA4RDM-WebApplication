let session_id = getCurrentSession();
let socket = io.connect('http://' + document.domain + ':' + location.port + '/api/run_process_discovery');

socket.on('updateColumnNames', function(response) {
    clearEverything();
    updateColumnNames(response);
});

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

function updateEverything() {
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

    socket.emit("update_xes_attributes", selectedColumns);
    return;
}

function updateColumnNames(allColumnNames) {
    // let selectinputTimestamp    = document.getElementById("timestamp_column");
    // let selectInputCaseId       = document.getElementById("caseId_column");
    // let selectInputActivity     = document.getElementById("activity_column");
    // let selectInputResource     = document.getElementById("resource_column");
    // let selectInputCost         = document.getElementById("cost_column");


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
    }

    // for (let columnName of allColumnNames){
    //     var opt = document.createElement('option');
    //     opt.value = columnName;
    //     opt.innerHTML = columnName;
    //     selectinputTimestamp.appendChild(opt);
    //     selectInputCaseId.appendChild(opt);
    //     selectInputActivity.appendChild(opt);
    //     selectInputResource.appendChild(opt);
    //     selectInputCost.appendChild(opt);
    // }
}

function getColumnNames() {
    socket.emit('requestColumnNames', session_id);
}

function updateDescriptiveStatistics(numberOfCases, numberOfEvents, numberOfActivities, numberOfVariants) {
    document.getElementById('description_number_of_cases').innerHTML        = numberOfCases;
    document.getElementById('description_number_of_events').innerHTML       = numberOfEvents;
    document.getElementById('description_number_of_activities').innerHTML   = numberOfActivities;
    document.getElementById('description_number_of_variants').innerHTML     = numberOfVariants;
}