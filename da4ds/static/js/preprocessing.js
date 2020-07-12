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

let dataSourceForm = document.getElementById('dataSourceSelectForm');
dataSourceForm.addEventListener('submit', function(event) {
    let dataSourceSelector = document.getElementById("dataSourceSelector");
    for (let option of dataSourceSelector.childNodes) {
        if (option.selected) {
            localStorage.setItem("selected_data_source", option.textContent);
        }
    }
});