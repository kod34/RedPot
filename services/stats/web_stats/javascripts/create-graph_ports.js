function parseData(createGraph) {
	Papa.parse("../csv_files/ports.csv", {
		download: true,
		complete: function(results) {
			createGraph(results.data);
		}
	});
}

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


var k = 'Arr';
var k2 = 'Att';
var ports = ['21', '22', '23', '25', '42', '53', '80', '88', '110', '119', '135', '137', '138', '138', '143', '443', '465', '993', '995', '1025', '3306'];
	
function createGraph(data) {

	var ips = [];
	var dates = [];
	var ttacks = [];
	var Arr=[];
	var Att= [];
	var Arrx = ['x'];
	var Arry = ['Frequency'];

	for (var i = 0; i < data.length-1; i++) {
		if (ports.indexOf(data[i][2]) !== -1 && data[i][4] !== 'local' && data[i][4] !== 'Error' && moment(data[i][0], "DD-MM-YYYY", true).isValid()){
			ttacks.push(data[i][2]);
			ips.push(data[i][4]);
			dates.push(data[i][0]);
		}
	}

	var result = foo(ips);	
	for (var i=0; i<result[0].length; i++){
		eval(k+i+'='+'['+'result[0][i]'+','+result[1][i]+'];');
		eval(k+'.push('+k+i+');');
	}

	var chart = c3.generate({
		size: {
        height: 480,
        width: 480
    },
	    data: {
	        columns: Arr,
	        type : 'pie',
	        pie: {
				expand: false
			},
	        onclick: function (d, i) { console.log("onclick", d, i); },
	        onmouseover: function (d, i) { console.log("onmouseover", d, i); },
	        onmouseout: function (d, i) { console.log("onmouseout", d, i); }
	    },
	    bindto: "#chart2"
	});


	var result = foo(ttacks);	
	for (var i=0; i<result[0].length; i++){
		eval(k2+i+'='+'['+'result[0][i]'+','+result[1][i]+'];');
		eval(k2+'.push('+k2+i+');');
	}

	var chart = c3.generate({
		size: {
        height: 400,
        width: 1050
    },
		data: {
			columns: Att,
            type: 'bar',
        },
        bar: {
        	space: 0.25,
        },
        axis: {
        	x: {
        		label: 'Port Number',
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
        bindto: '#chart'
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

	    bindto: '#chart3'
	});
	

}

function Live(){
	setTimeout("Live()", 10000);
	parseData(createGraph);
}