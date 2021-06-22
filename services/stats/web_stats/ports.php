<!DOCTYPE html>
<html>
	<head>
		<title>Ports</title>

		<!-- Load c3.css -->
		<link href="stylesheets/c3.css" rel="stylesheet" type="text/css">
		<link rel="shortcut icon" href="images/logo.ico" />

		<!-- Load d3.js and c3.js -->
		<script src="javascripts/d3.v3.min.js" charset="utf-8"></script>
		<script src="javascripts/c3.min.js"></script>

		<!-- Load papaparse.js -->
		<script src="javascripts/papaparse.min.js"></script>

		<!-- Load script -->
		<script src="javascripts/create-graph_ports.js"></script>

		<!-- Load moment script -->
		<script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.18.1/moment.min.js"></script>
  	</head>

  	<body onLoad="Live()">

  		<div class="vertical-menu">
		  <a href="index.php">Home</a>
		  <a href="traffic.php">Traffic</a>
		  <a href="ports.php" class="active"> Ports </a>
		  <a href="ssh_intrusions.php"> SSH </a>
		  <a href="web_intrusions.php"> Web Instrusions </a>
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
		<br><br><br>
		<div id="chart3"></div>
		<div id="title">
    	<div style="margin-left: 48%;">Ports Traffic</div>
    	<br>
    	<div class="port" >
    	<div id="chart"></div>
    	<div style="margin-left: 48%;" class = "">Ports Frequency</div>
    	<br>
    	<div id="chart2" style="margin-left: 40%;"></div>
    	<div style="margin-left: 48%;">Port Traffic Location</div>
		</div>
    	</div>

    	
    </div>

  	</body>

</html>
