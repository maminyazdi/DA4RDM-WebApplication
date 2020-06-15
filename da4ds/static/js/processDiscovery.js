let session_id = getCurrentSession();
let socket = io.connect('http://' + document.domain + ':' + location.port + '/api/run_process_discovery');
let hook = document.getElementById('data_target');

socket.on('updateColumnNames', function(response) {
    resetAllPMParameters();
    updateColumnNames(response);
    hideSpinner();
});

socket.on('processDiscoveryUpdateEverything', function(response) {
    resetAllPMParameters();
    updateEverything(response);
    hideSpinner();
})

socket.on('warning', function(response) {
    hideSpinner();
    hook.innerHTML = response['message'];
});

socket.on('info', function(response) {
    hook.innerHTML = response.message;
});

socket.on('gviz', function(response) {
    let relative_url = response.replace(/\\/g, "/");
    hideSpinner();
    hook.innerHTML = '';

    let link = document.createElement("a");
    link.href = window.location.protocol + "//" + window.location.host + "//" + relative_url;
    link.target = "_blank";

    let img = document.createElement("img");
    img.src = relative_url;

    // if the response is of type svg, the scale the svg to 1/2 view port, else add a container with 1/2 view port width and scroll to wrap the image
    let image_url_split = response.split('.');
    if (image_url_split[image_url_split.length - 1] === 'svg') {
        img.style.width = "50vw";
        img.style.height = "50vh";
    } else {
        let imgWrapper = document.createElement("div");
        imgWrapper.style.width = "50vw";
        imgWrapper.style.height = "50vw";
        imgWrapper.style.overflow = "scroll";
        hook.appendChild(imgWrapper);
        hook = imgWrapper;
    }

    link.style.cursor = "pointer";
    link.style.cursor = "-moz-zoom-in";
    link.style.cursor = "-webkit-zoom-in";
    link.style.cursor = "zoom-in";

    hook.appendChild(link);
    link.appendChild(img);
});

socket.on('dataframe_information_update', function(response){

});

socket.emit('requestDiscoveryPreparation', session_id);

function runProcessDiscovery(hostUrl, projectUrl){
    showSpinner();
    hook.innerHTML = "";
    let options = getDiscoveryOptions();
    socket.emit('requestProcessDiscovery', session_id, options);

    return;
}

function updateEverything(allDiscoveryInformation) {

    showSpinner();
    updateColumnNames(allDiscoveryInformation["all_column_names"], allDiscoveryInformation["pm_xes_attributes"]);
    updatePMFilters(allDiscoveryInformation["pm_filter_options"], allDiscoveryInformation["pm_filters"]);
    //update other options
    updateKeyMetrics(allDiscoveryInformation["pm_dataframe_key_metrics"])
    return;
}

function resetAllPMParameters() {
    document.getElementById('data_target').innerHTML = "";
    showSpinner();

    remove_all_options_from_select("timestamp_column");
    remove_all_options_from_select("caseId_column");
    remove_all_options_from_select("activity_column");
    remove_all_options_from_select("resource_column");
    remove_all_options_from_select("cost_column");

    remove_all_options_from_select("process_discovery_start_activity")
    remove_all_options_from_select("process_discovery_end_activity")

    clearDiscoveryMetrics();

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
    let selectedXesAttributeColumns = getXesAttributeColumns();
    socket.emit("requestDiscoveryPreparation", session_id, selectedXesAttributeColumns);
    return;
}

function sendPMParameters() {
    let selectedXesAttributeColumns = getXesAttributeColumns();
    let selectedPMFilters = getPMFilters();
    let selectedOptions = getDiscoveryOptions();

    socket.emit("requestDiscoveryPreparation",
                session_id,
                selectedXesAttributeColumns,
                selectedPMFilters,
                selectedOptions);
    return;
}

function sendDiscoveryReset() {
    resetAllPMParameters();
    socket.emit('requestDiscoveryReset', session_id);
}

function sendFiltersReset() {
    resetAllPMParameters();
    socket.emit('requestFilterReset', session_id);
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
    startDateSelect = document.getElementById('process_discovery_start_date');
    endDateSelect = document.getElementById('process_discovery_end_date');
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
        startActivitySelect.value = selectedFilters['process_discovery_start_activity']
    }
    if (selectedFilters['process_discovery_start_activity'] != undefined) {
        endActivitySelect.value = selectedFilters['process_discovery_start_activity']
    }

    minPerformanceSelect.value = (selectedFilters['process_discovery_min_performance'] !== undefined) ?
                                  selectedFilters['process_discovery_min_performance'] : '';
    maxPerformanceSelect.value = (selectedFilters['process_discovery_max_performance'] !== undefined) ?
                                  selectedFilters['process_discovery_max_performance'] : '';
}

function updateKeyMetrics(metrics) {
    document.getElementById('metrics_number_of_cases').innerHTML      = metrics["number_of_cases"];
    document.getElementById('metrics_number_of_events').innerHTML     = metrics["number_of_events"];
    document.getElementById('metrics_number_of_activities').innerHTML = metrics["number_of_activities"];
    document.getElementById('metrics_number_of_variants').innerHTML   = metrics["number_of_variants"];
}

function clearDiscoveryMetrics() {
    document.getElementById("metrics_number_of_cases").value = "";
    document.getElementById("metrics_number_of_events").value = "";
    document.getElementById("metrics_number_of_activities").value = "";
    document.getElementById("metrics_number_of_variants").value = "";
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
        if (current_select_input.tagName === 'SELECT') {
            selectedFilters[current_select_input.id] = getAllValuesFromMultiSelect(current_select_input)
        } else {
            selectedFilters[current_select_input.id] = current_select_input.value;
        }
    }

    return selectedFilters;
}

function getDiscoveryOptions() {
    algorithm      = document.getElementById('discovery_algorithm')
    representation = document.getElementById('model_represenations')
    variant        = document.getElementById('model_variant')
    options = {'discovery_algorithm': algorithm.value,
               'model_represenations': representation.value,
               'model_variant': variant.value}

    return options;
}

function getAllValuesFromMultiSelect(selectElement) {
    var selectedValues = [];
    var options = selectElement && selectElement.options;

    for (let opt of options) {
        if (opt.selected) {
            selectedValues.push(opt.value);
        }
    }
    return selectedValues;
}

function showSpinner() {
    let spinner = document.getElementById('discovery-spinner');
    spinner.style.display="block"
}

function hideSpinner() {
    let spinner = document.getElementById('discovery-spinner');
    spinner.style.display="none"
}