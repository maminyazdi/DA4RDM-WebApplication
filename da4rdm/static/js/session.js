
if (localStorage["sessionId"] === undefined) {
    createSession();

} else {
    updateSessionDisplay();
    //Added for SaveConfig (Second Approach)
    //var preprocessing = {"dataSourceSelector":"","project_name":"","pipelineParameters":"","data_source_name":""};
    var preprocessing = {};
    var provenance = {"timestamp_column":"","caseId_column":"","activity_column":"","resource_column":"","cost_column":"",
                        "discovery_algorithm":"","model_represenations":"","model_variant":""};

}

function createSession() {
    let isReset = false;
    if ('sessionId' in localStorage) {
        isReset = true;
    }
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/api/create_new_session');
    window.localStorage.clear();
    let sessionId = "";
    socket.emit('create_new_session');
    socket.on('session', function(data) {
        window.localStorage.setItem('sessionId', data);
        window.localStorage.setItem('selected_data_source', "None");
        window.localStorage.setItem('selected_pipeline', "None");
        document.getElementById("sessionCreatedCheckmark").style.display = "inline";
        updateSessionDisplay();
        if (isReset) {
            location.reload();
        }
    });
}

function addSessionIdToFormAction(formId) {
    let form = document.getElementById(formId);
    let hasQueryParameters = form.action.split('?').length > 1
    form.action = form.action +  (hasQueryParameters ? "&session_id=" : "?session_id=") + getCurrentSession()
}

function addSessioIdToReuqestUrl(elementId) {
    let element = document.getElementById(elementId);
    let hasQueryParameters = element.action.split('?').length > 1
    element.href = element.href + (hasQueryParameters ? "&session_id=" : "?session_id=") + getCurrentSession()
}

function getCurrentSession() {
    let session = window.localStorage.getItem("sessionId")
    return session
}

function updateSessionDisplay() {
    let pipelineDisplay = document.getElementById("user_session_pipeline_display");
    let dataSourceDisplay = document.getElementById("user_session_data_source_display");
    pipelineDisplay.innerHTML = localStorage["selected_pipeline"];
    dataSourceDisplay.innerHTML = localStorage["selected_data_source"];
    if (localStorage["selected_data_source"] != "None") {
        dataSourceDisplay.style.color = "black";
    }
}

//Added for SaveConfig
function insertData()
{
    var filename = document.getElementById('savedFileSelector');
    let socket = io.connect('http://' + document.domain + ':' + location.port + '/api/get_json'); //To get data from json file
    socket.emit('sendFileName',filename.value);
    socket.on('responseData',function(response){
         var output = JSON.parse(response);
         console.log(output)

        var currentTab = window.location.href;
        console.log(currentTab);

        if(currentTab.includes("process_discovery")){

            $('select[id=timestamp_column]').val(output["timestamp_column"]).change();
            $('select[id=caseId_column]').val(output["caseId_column"]).change();
            $('select[id=activity_column]').val(output["activity_column"]).change();
            $('select[id=cost_column]').val(output["cost_column"]).change();
            $('select[id=resource_column]').val(output["resource_column"]).change();
            $('select[id=discovery_algorithm]').val(output["discovery_algorithm"]).change();
            $('select[id=model_represenations]').val(output["model_represenations"]).change();
            $('select[id=model_variant]').val(output["model_variant"]).change();
        }

        else if(currentTab.includes("conformance")){

            document.getElementById("accept").checked = (output["#accept"] === 'true');
            document.getElementById("min").value = output["min"];
            document.getElementById("sec").value = output["sec"];
            //For operationSet1
            var opSet1 = output["actionSelect1"];
            var actionSelect1 = opSet1.split(",");
            document.getElementsByClassName("actionSelect1")[0].value = actionSelect1[0];
            var max1 = actionSelect1.length - 1;
            var x1 = 1;
            var container = $(".wraper1");
            var add = $(".add_icon1");
            while(x1 < max1) {
                    let object = actionSelect1[x1];
                    console.log("inside while");
                    console.log(x1,max1);
                    console.log("Action",actionSelect1[x1]);
                    var newElement = `<select class="form-control form-control-sm actionSelect1" id="operationSeq1">
                                                <option value="${object}" >${object}</option>
                                            </select>
                                        
                                        <div class="col"> 
                                        <button  type="button" class=" delete btn btn-outline-danger fa fa-times" ></button>
                                        </div>`;
                    $(container).append(newElement);
                    x1++;}

                    $(container).on("click",".delete",function(e){
                    e.preventDefault();
                    console.log("Inside Delete",this);
                    $(this).closest('.form-row').remove();
                    x1--;
                    })

                    //For OperationSet2
                    var opSet2 = output["actionSelect2"];
                    var actionSelect2 = opSet2.split(",");
                    document.getElementsByClassName("actionSelect2")[0].value = actionSelect2[0];
                    var max2 = actionSelect2.length - 1;
                    var x2 = 1;
                    var container2 = $(".wraper2");
                    var add2 = $(".add_icon2");
                    while(x2 < max2) {
                        let object2 = actionSelect1[x2];

                        var newElement2 = `<select class="form-control form-control-sm actionSelect2" id="operationSeq2">
                                                <option value="${object2}" >${object2}</option>
                                            </select>
                                        
                                        <div class="col"> 
                                        <button  type="button" class=" delete btn btn-outline-danger fa fa-times" ></button>
                                        </div>`;
                        $(container2).append(newElement2);
                        x2++;}

                        $(container2).on("click",".delete",function(e){
                        e.preventDefault();

                        $(this).closest('.form-row').remove();
                        x2--;
                        })
        }
        else if(currentTab.includes("visualization")){
            //ToDo something to load the information in less time. Currently it takes time to load information after pressing Upload.
            console.log("Inside Viz",output["pearsonWeighted"],output["pearsonBinary"],output["cosineWeighted"],output["cosineBinary"]);
            document.getElementById("pearsonWeighted").checked = (output["pearsonWeighted"] === 'true');
            document.getElementById("pearsonBinary").checked = (output["pearsonBinary"] === 'true');
            document.getElementById("cosineWeighted").checked = (output["cosineWeighted"] === 'true');
            document.getElementById("cosineBinary").checked = (output["cosineBinary"] === 'true');
            var projects = output["projectSelect"];
            var projectList = projects.split(",");
            var startDateList = output["startDate"].split(",");
            var endDateList = output["endDate"].split(",");
            console.log("viz",projectList,startDateList,endDateList);

            document.getElementsByClassName("projectSelect")[0].value = projectList[0];
            document.getElementsByClassName("startDate")[0].value = startDateList[0];
            document.getElementsByClassName("endDate")[0].value = endDateList[0];
            var max3 = projectList.length - 1;
            var x3 = 1;
            var container3 = $(".wraper1");
            console.log("visualization",max3,x3);
            while(x3 < max3) {
	            let object3 = projectList[x3];
                let startDate = startDateList[x3];
                let enddate = endDateList[x3];
                var newElement3 = `<select class="form-control form-control-sm projectSelect" id="projectid" onchange="myFunction()">
								        <option value="${object3}" >${object3}</option>
							        </select>
                                    <input type="date" class="startDate" id="date1" name="date1" value="${startDate}">
                                    <input type="date" class="endDate" id="date2" name="date2" value="${enddate}">`;
	            $(container3).append(newElement3);
	            x3++;}
                $(container3).on("click",".delete",function(e){
	            e.preventDefault();
	            console.log("Inside Delete",this);
	            $(this).closest('.form-row').remove();
	            x3--;
	            })

        }
        else{
            document.getElementById('dataSourceSelector').value = output["dataSourceSelector"];
         document.getElementById('user_session_data_source_display').value = output["dataSourceSelector"];
        $('select[name=project_name]').val(output["project_name"]);
        document.getElementById('pipelineParameters').value = output["pipelineParameters"];
        }
});
}