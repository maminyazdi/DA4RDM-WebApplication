function createSession() {
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/api/create_new_session');
    window.localStorage.clear();
    let sessionId = "";
    socket.emit('create_new_session');
    socket.on('session', function(data) {
        window.localStorage.setItem('sessionId', data)
    });
}