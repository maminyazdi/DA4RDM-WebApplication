function downloadWorkingData() {
    let currentSession = getCurrentSession();
    var base_url = window.location.origin;

    axios.get(base_url + '/api/download_temporary_data?session_id=' + currentSession)
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
