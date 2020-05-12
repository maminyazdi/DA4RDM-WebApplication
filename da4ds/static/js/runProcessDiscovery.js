let socket = socket = io.connect('http://' + document.domain + ':' + location.port + '/api/run_process_discovery');


function runProcessDiscovery(hostUrl, projectUrl){
    let session_id = getCurrentSession();
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

function updateFilters() {
    return;
}

function sendFilters() {
    return;
}

function sendStartAndEndDate() {

}

function sendMetaDecisions() {
    return;
}

function sendKeyKolumnChoice() {
    return;
}

function getColumnNames() {

}

function updateDescriptiveStatistics(numberOfCases, numberOfEvents, numberOfActivities, numberOfVariants) {
    document.getElementById('description_number_of_cases').innerHTML        = numberOfCases;
    document.getElementById('description_number_of_events').innerHTML       = numberOfEvents;
    document.getElementById('description_number_of_activities').innerHTML   = numberOfActivities;
    document.getElementById('description_number_of_variants').innerHTML     = numberOfVariants;
}