let sessionId = getCurrentSession();
let socket = io.connect('http://' + document.domain + ':' + location.port + '/api/conformance');

//Event on Select button
let operationSeqSetFrom= document.getElementById('operationSeqSetFrom');
operationSeqSetFrom.addEventListener('submit', function(event) {
	event.preventDefault();
	let minutes = document.getElementById("min");
	let seconds = document.getElementById("sec");
	let actions1 = document.getElementsByClassName("actionSelect1");
	let actions2 = document.getElementsByClassName("actionSelect2");
	let actionList1 = '';
	let actionList2 = '';
	//For getting values from multiple drop-downs
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

function updateResponse(Output) {
	document.getElementById('no_of_nonConforming_cases').innerHTML      = Output["NonConformingCases"];
	document.getElementById('Result').innerHTML      = JSON.stringify(Output["JSON_Response"]);
	document.getElementById('total_number_of_cases').innerHTML = Output["TotalNoOfCases"];
	document.getElementById('dataSet_start_time').innerHTML = Output["dataSet_start_time"];
	document.getElementById('dataSet_end_time').innerHTML = Output["dataSet_end_time"];
	console.log(JSON.stringify(Output["JSON_Response"]));
}
