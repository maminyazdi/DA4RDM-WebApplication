let sessionId = getCurrentSession();
let socket = io.connect('http://' + document.domain + ':' + location.port + '/api/visualization');

let visualizationFrom= document.getElementById('visualizationFrom');
visualizationFrom.addEventListener('submit', function(event) {
  event.preventDefault();

  let startDate = document.getElementsByClassName("startDate");
  let endDate = document.getElementsByClassName("endDate");

  let pearsonWeighted = (document.querySelector('#pearsonWeighted')).checked;
  let pearsonBinary = (document.querySelector('#pearsonBinary')).checked;
  let cosineWeighted = (document.querySelector('#cosineWeighted')).checked;
  let cosineBinary = (document.querySelector('#cosineBinary')).checked;
  let projects = document.getElementsByClassName("projectSelect");
  let projectList = '';
  let startDateList = '';
  let endDateList = '';


  for(var i=0;i<projects.length;i++){
		projectList = projectList + projects[i].value + ',';
        startDateList = startDateList + startDate[i].value + ',';
        endDateList = endDateList + endDate[i].value + ',';
	}

  socket.emit('visualizationTest',sessionId,projectList,startDateList,endDateList,
      {'PearsonWeighted': pearsonWeighted,'PearsonBinary':pearsonBinary,'CosineWeighted':cosineWeighted,
      'CosineBinary':cosineBinary})
});

socket.on('radarChart',function(response) {

  plotChart(response)
})

function plotChart(output){

document.getElementById("run").addEventListener("click", function() {

myRadarChart.destroy();
radarChart2.destroy();
});
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
	var radarChart = $('#Pearson');
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
    var data2 = {
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
    var cosineRadarChart = $('#Cosine');
	var radarChart2 = new Chart(cosineRadarChart, {
	  type: "radar",
	  data: data2,
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
    //window.alert(typeof(Object.values(responseChart)));
    for (var [key,value] of Object.entries(responseChart)) {

        if (value.length > 0){
            if(key.includes("Pearson")){
            myRadarChart.data.datasets.push({
            label: key + ' Project' + (i+1),
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
            if(key.includes("Cosine")){
             radarChart2.data.datasets.push({
            label: key + ' Project' + (i+1),
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

        }

    }

		myRadarChart.update();
        radarChart2.update();
}
}
}