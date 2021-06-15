<!DOCTYPE html>
<html>
	<head>
		<title>Web Intrusions</title>

		<!-- Load c3.css -->
		<link href="stylesheets/c3.css" rel="stylesheet" type="text/css">

		<!-- Load d3.js and c3.js -->
		<script src="javascripts/d3.v3.min.js" charset="utf-8"></script>
		<script src="javascripts/c3.min.js"></script>

		<!-- Load papaparse.js -->
		<script src="javascripts/papaparse.min.js"></script>

		<!-- Load script -->
		<script src="javascripts/create-graph_web.js"></script>
  	</head>

  	<body onLoad="Live()">

  		<div class="vertical-menu">
		  <a href="index.php">Home</a>
		  <a href="ports.php"> Ports </a>
		  <a href="ssh_intrusions.php"> SSH </a>
		  <a href="web_intrusions.php" class="active"> Web Instrusions </a>
		</div>


		<div class="card-body row" style="padding:0px;margin-top:20px;margin-left:120px;margin-right:120px">
  		<div class="col border-line">
   		<div class="row justify-content-center">
    	</div>
 	    <div class="row">
  		</div>
  		</div>

	<br><br>
    	
	<div class="container">
		<div id="title">
			<div id="chart2"></div>
			<div style="margin-left: 48%;">Frequency of Attacks</div>
		</div>
			<br><br>
		<div id="title">
			<div id="chart" class="pie_int"></div>
			<div style="margin-left: 48%;">Sources of Attack</div>
		</div>
			<br><br>
		<div id="title">
			<div id="chart3" class="lol"></div>
			<div style="margin-left: 48%;">Types of Attacks</div>
		</div>
			<br><br>
	</div>

  	</body>

</html>
