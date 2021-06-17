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

function createGraph(data) {
	var ips = [];
	for (var i = 0; i < data.length-1; i++) {
		ips.push(data[i][4])
	}

	var Arr=[];
	var k = 'Arr';
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
	    },
	    bindto: "#chart2"
	});

	var ttacks = [];
	for (var i = 0; i < data.length-1; i++) {
		ttacks.push(data[i][2])
	}

	var Att=[];
	var k = 'Att';
	var result = foo(ttacks);	
	for (var i=0; i<result[0].length; i++){
		eval(k+i+'='+'['+'result[0][i]'+','+result[1][i]+'];');
		eval(k+'.push('+k+i+');');
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
        bindto: '#chart'
	});
	

}

function Live(){
	setTimeout("Live()", 10000);
	parseData(createGraph);
}