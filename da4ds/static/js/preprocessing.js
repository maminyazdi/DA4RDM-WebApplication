let sessionId = getCurrentSession();
let socket = io.connect('http://' + document.domain + ':' + location.port + '/api/preprocessing');

setup();

socket.on('preprocessingStatus', function (response) {
    if (response['task'] = 'read' && response['result'] == 'success') {
        let dataSourceName = response['data_source_name'];
        onDatasourceSelected(dataSourceName);
    }
})

function setup() {
    if (localStorage && 'selected_data_source' in localStorage && localStorage['selected_data_source'] && localStorage['selected_data_source'] != 'None') {
        document.getElementById('pipeline_actions').disabled = false;
    }
}

function onDatasourceSelected(dataSourceName) {
    document.getElementById('pipeline_actions').disabled = false;
    localStorage.setItem("selected_data_source", dataSourceName);
    document.getElementById("user_session_data_source_display").innerHTML = dataSourceName;
}

function downloadWorkingData(fileName) {
    let currentSession = getCurrentSession();
    var base_url = window.location.origin;

    axios.get(base_url + '/api/download_temporary_data?session_id=' + currentSession + '&requested_file=' + fileName)
    .then(function (response) {
        // handle success
        console.log(response);
    })
    .catch(function (error) {
        // handle error
        console.log(error);
    })
    .then(function () {
        // always executed
    });
    return
}

let dataSourceForm = document.getElementById('dataSourceSelectForm');
dataSourceForm.addEventListener('submit', function(event) {
    event.preventDefault();
    let dataSourceSelector = document.getElementById("dataSourceSelector");
    socket.emit('requestReadDataFromSource', sessionId, {'data_source_id': dataSourceSelector.value})
});