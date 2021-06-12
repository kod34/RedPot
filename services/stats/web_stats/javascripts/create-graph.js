function parseData(createGraph) {
	Papa.parse("/redpot/logs/csv_files/fakessh.csv", {
		download: true,
		complete: function(results) {
			createGraph(results.data);
		}
	});
}

function createGraph(data) {
	var ips = [];

	for (var i = 0; i < data.length-1; i++) {
		ips.push(data[i][3])
	}

	var Arr=[];
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
}

function Live(){
	setTimeout("Live()", 1000);
	parseData(createGraph);
}
