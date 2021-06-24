document.getElementById("csv_radio").addEventListener('change', function() {
    document.getElementById("data_source_upload").style.display = "block";
    document.getElementById("csv_parameter_description").style.display = "block";
    document.getElementById("database_parameter_description").style.display = "none";
});

document.getElementById("xes_radio").addEventListener('change', function() {
    document.getElementById("data_source_upload").style.display = "block";
    document.getElementById("csv_parameter_description").style.display = "none";
    document.getElementById("database_parameter_description").style.display = "none";
});

document.getElementById("database_radio").addEventListener('change', function() {
    document.getElementById("data_source_upload").style.display = "block";
    document.getElementById("csv_parameter_description").style.display = "none";
    document.getElementById("database_parameter_description").style.display = "block";
});

dataSourceRadios = document.getElementsByClassName('data_source_radio');
for (let radio of dataSourceRadios) {
    if (radio.id !== 'csv_radio' && radio.id !== 'xes_radio') {
        radio.addEventListener('change', function() {
            document.getElementById("data_source_upload").style.display = "none";
        });
    }
}
