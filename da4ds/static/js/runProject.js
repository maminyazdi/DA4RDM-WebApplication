function runProject(hostUrl, projectUrl, projectName){
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/api/run_project');
    let spinner = document.getElementById('pipeline-running-spinner');
    spinner.style.display="block"
    socket.emit('requestProjectRun', {'projectName': projectName});
    socket.on('progressLog', function(data) {
        let hook = document.getElementById('data_target');
        hook.textContent = data.message;
    });
    socket.on('json', function(response) {
        let hook = document.getElementById('data_target');
        spinner.style.display="none";
        visualize(response);
    })
}

function visualize(response) {
    let hook = document.getElementById('data_target');

    if (response.kind == "table") {
        hook.style.width = '90em';
        hook.style.height = '40em';

        google.charts.load('current', {'packages':['table']});
        google.charts.setOnLoadCallback(drawTable);

        parsedData = JSON.parse(response.data);
        let formattedData = [];

        columnArray = [];
        columnArray[0] = {label: parsedData.columns[0], type: 'string'};
        for (let i=1; i<parsedData.columns.length; ++i) {
            columnArray[i] = {label: parsedData.columns[i], type: 'number'}
        }

        formattedData[0] = columnArray;
        formattedData = formattedData.concat(parsedData.data)

        function drawTable() {

            var datatable = new google.visualization.arrayToDataTable(formattedData);
            var table = new google.visualization.Table(hook);
            table.draw(datatable, {showRowNumber: true, page:'enable', pageSize:50, frozenColumns:1, width: '90em', height: '40em'});

        }

        // var datatable = new google.visualization.DataTable(response.data);
        // var table = new google.visualization.Table(document.getElementById('data_target'));
        // table.draw(datatable, {showRowNumber: true, width: '100%', height: '100%'});

        // d3.json('C:/Temp/testjson.json', function (error,flu) {
        //     console.log(flu);
        //     return flu;
        //});

        /*
        data = JSON.parse(response.data);
        columnNames = getColumnNames(data);
        dataContent = createJsonArray(data, columnNames)
        console.log(data);
        tabulate(dataContent, columnNames)*/
    } else if (response.kind === 'barCharts') {
        hook.style.width = '90em';
        hook.style.height = '40em';

        google.charts.load('current', {'packages':['bar']});
        google.charts.setOnLoadCallback(drawChart);

        function drawChart() {
            var data = google.visualization.arrayToDataTable(response.data);

            var options = {
                chart: {
                title: response.options.title,
                subtitle: response.options.subtitle,
                },
                bars: 'vertical' // Required for Material Bar Charts.
            };

            var chart = new google.charts.Bar(hook);

            chart.draw(data, google.charts.Bar.convertOptions(options));
        }


    } else if (response.kind === 'text') {
        let hook = document.getElementById('data_target');
        hook.textContent = response.data;
    }
}

function getColumnNames(data) {
    columnNames = [];
    for (datum in data) {
        columnNames.push(datum);
    }
    console.log(columnNames);
    return columnNames;
}

function createJsonArray(data, columnNames) {
    dataContent = [];
    columnNames.forEach(function(columnName) {
        dataContent.push(data[columnName]);
    })
    console.log(dataContent);
    return dataContent;
}

function tabulate(data, columns) {
    var table = d3.select('#data_target').append('table')
    var thead = table.append('thead')
    var	tbody = table.append('tbody');

    // append the header row
    thead.append('tr')
      .selectAll('th')
      .data(columns).enter()
      .append('th')
        .text(function (column) { return column; });

    // create a row for each object in the data
    var rows = tbody.selectAll('tr')
      .data(data)
      .enter()
      .append('tr');

    // create a cell in each row for each column
    var cells = rows.selectAll('td')
      .data(function (row) {
        return columns.map(function (column) {
          return {column: column, value: row[column]};
        });
      })
      .enter()
      .append('td')
        .text(function (d) { return d.value; });

  return table;
}
