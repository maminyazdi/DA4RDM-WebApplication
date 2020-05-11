function runProcessDiscovery(hostUrl, projectUrl){
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/api/run_process_discovery');
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

function sendMetaDecisions() {
    return;
}

function sendKeyKolumnChoice() {
    return;
}

function getColumnNames() {

}