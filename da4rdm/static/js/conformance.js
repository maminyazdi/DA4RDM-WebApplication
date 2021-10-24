let sessionId = getCurrentSession();
let socket = io.connect('http://' + document.domain + ':' + location.port + '/api/conformance');

let operationSeqSetFrom= document.getElementById('operationSeqSetFrom');
operationSeqSetFrom.addEventListener('submit', function(event) {
	event.preventDefault();
	//let OpSeqSet1 = document.getElementById("OpSeqSet1");
	//let OpSeqSet2 = document.getElementById("OpSeqSet2");
	//let performance = document.getElementById("timespan");
	let minutes = document.getElementById("min");
	let seconds = document.getElementById("sec");
	//let actionSet = document.getElementById("actionSelect");
	let temp = document.getElementById("OperationSeq");
	let actions1 = document.getElementsByClassName("actionSelect1");
	let actions2 = document.getElementsByClassName("actionSelect2");
	let actionList1 = '';
	let actionList2 = '';
	for(var i=0;i<actions1.length;i++){
		actionList1 = actionList1 + actions1[i].value + ',';
	}
	for(var i=0;i<actions2.length;i++){
		actionList2 = actionList2 + actions2[i].value + ',';
	}

	socket.emit('requestReadOperationSeqSet', sessionId,actionList1,actionList2,{'min': minutes.value,'sec':seconds.value})
});

socket.on('conformanceCheckingOP',function(response) {
	updateResponse(response)
})

function updateResponse(jsonOutput) {
	document.getElementById('metrics_number_of_variants1').innerHTML      = jsonOutput["NonConformingCases"];
	document.getElementById('OP').innerHTML      = JSON.stringify(jsonOutput["JSON_Response"]);
}
