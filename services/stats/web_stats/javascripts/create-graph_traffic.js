function parseData(createGraph) {
	Papa.parse("../csv_files/traffic.csv", {
		download: true,
		complete: function(results) {
			createGraph(results.data);
		}
	});
}

var k = 'Arr';

function foo(arr) {
	  var a = [],
	    b = [],
	    prev;
	  arr.sort();
	  for (var i = 0; i < arr.length; i++) {
	    if (arr[i] !== prev) {
	      a.push(arr[i]);
	      b.push(1);
	    } else {
	      b[b.length - 1]++;
	    }
	    prev = arr[i];
	  }
	  return [a, b];
	}

function createGraph(data) {

	var Arrx = ['x'];
	var Arry = ['Frequency'];
	var dates = [];

	for (var i = 0; i < data.length-1; i++) {
		dates.push(data[i][0]);
	}

	var result = foo(dates);	

	for (var i = 0; i < result[0].length; i++){
		Arrx.push(result[0][i]);
		Arry.push(result[1][i]);
	}

	var chart = c3.generate({
		size: {
			width: 1050
		},
		data: {
			x: 'x',
			xFormat: '%d-%m-%Y',
			columns: [Arrx,Arry]
		},
	    axis: {
	        x: {
	        	label: 'Date',
	            type: 'timeseries',
	            tick: {
	                format: '%d-%m-%Y'
	            }
	        },
	        y: {
	        	label: 'Frequency'
	        }
	    },
	    zoom: {
	    	enabled: true
	    },

	    bindto: '#chart'
	});

}

function Live(){
	setTimeout("Live()", 10000);
	parseData(createGraph);
}