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
	document.getElementById('total_number_of_cases').innerHTML = Output["TotalNoOfCases"];
	document.getElementById('dataSet_start_time').innerHTML = Output["dataSet_start_time"];
	document.getElementById('dataSet_end_time').innerHTML = Output["dataSet_end_time"];

	$(".scrollBox").css("display", "none");
	$('#accordion').empty()
	var container = $("#accordion");



	if ( Output["JSON_Response"].length !== 0 ){
		$(".scrollBox").css("display", "block");
		for ( let i=0;i<Output["JSON_Response"].length;i++){
			let object = Output["JSON_Response"][i];
			var accordionElement = ` <div class="card">
	                                    <div class="card-header" id="heading${i}">
	                                      <h5 class="mb-0">
	                                        <button class="btn btn-link" data-toggle="collapse" data-target="#collapse${i}" aria-expanded="true" aria-controls="collapse${i}">
	                                           Case ${i+1}
	                                        </button>
	                                      </h5>
	                                    </div>
												
	                                    <div id="collapse${i}" class="collapse " aria-labelledby="heading${i}" data-parent="#accordion">
	                                      <div class="card-body">
	                                      	<span style="display: block;">
	                                      		<b>Operation: </b>${object.Operation}
											</span>
											<span style="display: block;">
	                                      		<b>Timestamp: </b>${object.Timestamp}
											</span>
	                                      	<span style="display: block;">
	                                      		<b>User Id: </b>${object.UserId}
											</span>
	                                      	<span style="display: block;">
	                                      		<b>Role Id: </b>${object.RoleId}
											</span>
											<span style="display: block;">
	                                      		<b>Project Id: </b>${object.ProjectId}
											</span>
											<span style="display: block;">
	                                      		<b>Resource Id: </b>${object.ResourceId}
											</span>
											<span style="display: block;">
	                                      		<b>File Id: </b>${object.FileId}
											</span>
									      </div>
	                                    </div>
	                                  </div>` ;

			$(container).append(accordionElement);
		}
	}
	// console.log(JSON.stringify(Output["JSON_Response"]));

}
