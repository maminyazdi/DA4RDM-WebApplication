let sessionId = getCurrentSession();
let socket = io.connect('http://' + document.domain + ':' + location.port + '/api/visualization');

let visualizationFrom= document.getElementById('visualizationFrom');
visualizationFrom.addEventListener('submit', function(event) {
  event.preventDefault();

  let projectId = document.getElementById("projectid");
  let startDate = document.getElementById("date1");
  let endDate = document.getElementById("date2");

  let pearsonWeighted = (document.querySelector('#pearsonWeighted')).checked;
  let pearsonBinary = (document.querySelector('#pearsonBinary')).checked;
  let cosineWeighted = (document.querySelector('#cosineWeighted')).checked;
  let cosineBinary = (document.querySelector('#cosineBinary')).checked;
  let projects = document.getElementsByClassName("projectSelect");
  let projectList = '';

  for(var i=0;i<projects.length;i++){
		projectList = projectList + projects[i].value + ',';
	}

  socket.emit('visualizationTest',sessionId,projectList,startDate.value,endDate.value,
      {'PearsonWeighted': pearsonWeighted,'PearsonBinary':pearsonBinary,'CosineWeighted':cosineWeighted,
      'CosineBinary':cosineBinary})
});

socket.on('radarChart',function(response) {
   //myRadarChart.destroy();
  plotChart(response)
})

function plotChart(output){
//window.alert(typeof output);
//window.alert(Object.getOwnPropertyNames(output));
//window.alert(Object.values(output));

var data1 = {
      labels: [
        'Planning',
        'Procedure',
        'Analysis',
        'Archival',
        'Access',
        'Re-Use'
      ],
      datasets: [
	  ]
    };
	var radarChart = $('#myChart');
	var myRadarChart = new Chart(radarChart, {
	  type: "radar",
	  data: data1,
	  options: {
	  elements: {
		  line: {
			borderWidth: 3
		  }
		}
	  }
	});
if (output["Similarity_Response"].length !== 0){
for (let i = 0; i < output["Similarity_Response"].length; i++){
	var responseChart = output["Similarity_Response"][i];
    window.alert(Object.values(responseChart));
    //r = 50 + 30 * i
    //g = 80 + 20 * i
    //b = 75 + 15 * i

    for (var [key,value] of Object.entries(responseChart)) {
        myRadarChart.data.datasets.push({
            label: key + 'Project' + i,
            data: value,
            fill: true,
            backgroundColor: 'rgba(50, 70, 50, 0.2)',
            borderColor: 'rgb(255, 99, 132)',
            pointBackgroundColor: 'rgb(255, 99, 132)',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: 'rgb(255, 99, 132)'
        });
    }

		myRadarChart.update();


}
}
}