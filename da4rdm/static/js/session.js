if (localStorage["sessionId"] === undefined) {
    createSession();
} else {
    updateSessionDisplay();
}

function createSession() {
    let isReset = false;
    if ('sessionId' in localStorage) {
        isReset = true;
    }
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/api/create_new_session');
    window.localStorage.clear();
    let sessionId = "";
    socket.emit('create_new_session');
    socket.on('session', function(data) {
        window.localStorage.setItem('sessionId', data);
        window.localStorage.setItem('selected_data_source', "None");
        window.localStorage.setItem('selected_pipeline', "None");
        document.getElementById("sessionCreatedCheckmark").style.display = "inline";
        updateSessionDisplay();
        if (isReset) {
            location.reload();
        }
    });
}

function addSessionIdToFormAction(formId) {
    let form = document.getElementById(formId);
    let hasQueryParameters = form.action.split('?').length > 1
    form.action = form.action +  (hasQueryParameters ? "&session_id=" : "?session_id=") + getCurrentSession()
}

function addSessioIdToReuqestUrl(elementId) {
    let element = document.getElementById(elementId);
    let hasQueryParameters = element.action.split('?').length > 1
    element.href = element.href + (hasQueryParameters ? "&session_id=" : "?session_id=") + getCurrentSession()
}

function getCurrentSession() {
    let session = window.localStorage.getItem("sessionId")
    return session
}

function updateSessionDisplay() {
    let pipelineDisplay = document.getElementById("user_session_pipeline_display");
    let dataSourceDisplay = document.getElementById("user_session_data_source_display");
    pipelineDisplay.innerHTML = localStorage["selected_pipeline"];
    dataSourceDisplay.innerHTML = localStorage["selected_data_source"];
    if (localStorage["selected_data_source"] != "None") {
        dataSourceDisplay.style.color = "black";
    }
}