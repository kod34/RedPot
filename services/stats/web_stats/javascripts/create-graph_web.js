function parseData(createGraph) {
	Papa.parse("../csv_files/intrusions.csv", {
		download: true,
		complete: function(results) {
			createGraph(results.data);
		}
	});
}

var k = 'Arr';
var c = 'Att';

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
	var ips = [];
	var dates = [];
	var Arrx = ['x'];
	var Arry = ['Attacks'];
	var ttacks = [];
	var Att=[];
	var Arr=[];

	for (var i = 0; i < data.length-1; i++) {
		ips.push(data[i][4]);
		dates.push(data[i][0]);
		ttacks.push(data[i][2]);
	}


	var result = foo(ips);	
	for (var i=0; i<result[0].length; i++){
		eval(k+i+'='+'['+'result[0][i]'+','+result[1][i]+'];');
		eval(k+'.push('+k+i+');');
	}

	var chart = c3.generate({
	    data: {
	        columns: Arr,
	        type : 'pie',
	        onclick: function (d, i) { console.log("onclick", d, i); },
	        onmouseover: function (d, i) { console.log("onmouseover", d, i); },
	        onmouseout: function (d, i) { console.log("onmouseout", d, i); }
	    }
	});


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

	    bindto: '#chart2'
	});

	var result = foo(ttacks);
	for (var i=0; i<result[0].length; i++){
		eval(c+i+'='+'['+'result[0][i]'+','+result[1][i]+'];');
		eval(c+'.push('+c+i+');');
	}


	var chart = c3.generate({
		data: {
			columns: Att,
            type: 'bar',
        },
        bar: {
        	space: 0.25,
        },
        axis: {
        	x: {
        		label: 'Attack Type',
        		type: 'category',
            	categories: ['']
        	},
        	y: {
        		label: 'Frequency'
        	}
        },
        zoom: {
	    	enabled: true
	    },
        bindto: '#chart3'
	});

}

function Live(){
	setTimeout("Live()", 10000);
	parseData(createGraph);
}