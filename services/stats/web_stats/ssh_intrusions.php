<!DOCTYPE html>
<html>
	<head>
		<title>SSH Intrusions</title>

		<meta name="viewport" content="width=device-width, initial-scale=1">
		<link rel="shortcut icon" href="images/logo.ico" />

		<!-- Load c3.css -->
		<link href="stylesheets/c3.css" rel="stylesheet" type="text/css">

		<!-- Load d3.js and c3.js -->

		<script src="javascripts/d3.v3.min.js" charset="utf-8"></script>
		<script src="javascripts/c3.min.js"></script>

		<!-- Load papaparse.js -->
		<script src="javascripts/papaparse.min.js"></script>

		<!-- Load script -->
		<script src="javascripts/create-graph_ssh.js"></script>

  	</head>

  	<body onLoad="Live()">


		<div class="vertical-menu">
		  <a href="index.php">Home</a>
		  <a href="traffic.php">Traffic</a>
		  <a href="ports.php"> Ports </a>
		  <a href="ssh_intrusions.php" class="active"> SSH </a>
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
			<div id="title">
			<div id="chart2"></div>
    		<div style="margin-left: 48%;">Frequency of Attacks</div>
    		</div>
			<br><br>
			<div id="title">
			<div id="chart" class="pie"></div>
			<div style="margin-left: 48%;">Sources of Attack</div>
		</div>

			<br><br>
		</div>
	</body>

</html>
