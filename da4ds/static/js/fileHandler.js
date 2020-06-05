function downloadFile(requestedFile) {
    let currentSession = getCurrentSession();
    var base_url = window.location.origin;

    axios({
        method: 'get',
        url: base_url + '/api/download_temporary_data?session_id=' + currentSession + "&requested_file=" + requestedFile,
        responseType: 'blob'
    })
    .then(function(response) {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        const contentDisposition = response.request.getResponseHeader('Content-Disposition');
        const fileName = contentDisposition.split(';')[1].trim().split('=')[1].trim();
        link.href = url;
        link.setAttribute('download', fileName);
        document.body.appendChild(link);
        link.click();
    });
}

function uploadFile() {
    return true;
}
