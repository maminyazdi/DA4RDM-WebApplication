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

document.getElementById("csv_radio").addEventListener('change', function() {
    document.getElementById("data_source_upload").style.display = "block";
});
document.getElementById("xes_radio").addEventListener('change', function() {
    document.getElementById("data_source_upload").style.display = "block";
});

dataSourceRadios = document.getElementsByClassName('data_source_radio');
for (let radio of dataSourceRadios) {
    if (radio.id !== 'csv_radio' && radio.id !== 'xes_radio') {
        radio.addEventListener('change', function() {
            document.getElementById("data_source_upload").style.display = "none";
        });
    }
}