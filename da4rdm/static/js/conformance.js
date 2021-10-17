let sessionId = getCurrentSession();
let socket = io.connect('http://' + document.domain + ':' + location.port + '/api/conformance');

let operationSeqSetFrom= document.getElementById('operationSeqSetFrom');
operationSeqSetFrom.addEventListener('submit', function(event) {
	event.preventDefault();
	let OpSeqSet1 = document.getElementById("OpSeqSet1");
	let OpSeqSet2 = document.getElementById("OpSeqSet2");
	let performance = document.getElementById("timespan");
	socket.emit('requestReadOperationSeqSet', sessionId, {'op_seq_set1': OpSeqSet1.value})
});