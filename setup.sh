#!/bin/bash
set -e
if [[ $EUID -ne 0 ]];then
	echo "[!] The Script must be run as Root!"
	exit 1
fi
echo ---------------------------------------------------------------------
echo ‎‎‎WARNING: Setting up the vulnerable environment might cause data loss!
echo ---------------------------------------------------------------------
sleep 1
echo 
read -p 'Do you wish to continue? (Y/n) ' continue
case $continue in 
	n|N|No|no|No)
	exit 1
	;;

	y|Y|yes|Yes|YES)
	echo -------------------------------------------------------------------
	echo ‎‎‎‎'                    'Configuring Environment
	echo -------------------------------------------------------------------
	echo [+] Creating directory /redpot
	rm -r /redpot ||:
	mkdir -p /redpot
	sleep 1
	echo [+] Creating log directory /redpot/logs
	mkdir -p /redpot/logs
	sleep 1
	echo [+] Done
	echo -------------------------------------------------------------------
	echo ‎‎‎‎‎‎‎‎‎‎'                       'Configuring Website
	echo -------------------------------------------------------------------
	# read -p 'The Port Where The Webserver Should Run On: ' port
	# while ! [[ $port =~ ^[0-9]+$ ]] || [ $port -gt 49151 ]
	# do
 	#   	echo "Error: Invalid Port"
 	#   	read -p 'The Port Where The Webserver Should Run On: ' port
 	# done
	echo [+] Creating directory /redpot/apache
	mkdir -p /redpot/apache
	sleep 1
	echo
	echo "Website Templates Available: "
	echo 
	echo 1 : bootstrap-shop
	echo 2 : digishop-mini
	echo
	read -p "Which template would you like to use? " template
	case $template in
		1|One|bootstrap-shop)
		echo [+] Downloading website files...
		wget -P /redpot/apache https://www.free-css.com/assets/files/free-css-templates/download/page194/bootstrap-shop.zip
		echo [+] Extracting files...
		unzip /redpot/apache/bootstrap-shop.zip -d /redpot/apache/
		echo [+] Copying files to /var/www/html
		cp -r /redpot/apache/bootstrap-shop/* /var/www/html/
		sleep 1
		# echo [+] Configuring Ports...
		# sed -i '5s/.*/Listen '$port'/' /etc/apache2/ports.conf
		# sed -i '1s/.*/<VirtualHost *:'$port'>/' /etc/apache2/sites-available/000-default.conf
		# sleep 1
		echo [+] Configuring hostnames file /etc/hosts... 
		echo "127.0.0.1 bootstrap-shop.com www.bootstrap-shop.com" >> /etc/hosts
		sleep 1
		echo [+] Starting the Apache server...
		systemctl restart apache2
		echo [+] Done
		echo [*] Fake website url: http://bootstrap-shop.com
		;;

		2|Two|digishop-mini)
		echo [+] Creating directory /redpot/apache
		mkdir -p /redpot/apache
		sleep 1
		echo [+] Downloading website files...
		wget -P /redpot/apache https://www.free-css.com/assets/files/free-css-templates/download/page201/digishop-mini.zip
		echo [+] Extracting files...
		unzip /redpot/apache/digishop-mini.zip -d /redpot/apache/
		echo [+] Copying files to /var/www/html
		cp -r /redpot/apache/bs-digishop-mini/* /var/www/html/
		sleep 1
		# echo [+] Configuring Ports...
		# sed -i '5s/.*/Listen '$port'/' /etc/apache2/ports.conf
		# sed -i '1s/.*/<VirtualHost *:'$port'>/' /etc/apache2/sites-available/000-default.conf
		# sleep 1
		echo [+] Configuring hostnames file /etc/hosts... 
		echo "127.0.0.1 digishop-mini.com www.digishop-mini.com" >> /etc/hosts
		sleep 1
		echo [+] Starting the Apache server...
		systemctl restart apache2
		echo [+] Done
		echo [*] Fake website url: http://digishop-mini.com
		;;
		*)
		echo [-] Unknown Option
		echo [-] Exiting...
		sleep 1
		exit 1
		;;
	esac
	echo -------------------------------------------------------------------
	echo ‎‎‎‎'                    'Configuring SSH Server
	echo -------------------------------------------------------------------
	# read -p 'The Port Where The SSH Server Should Run On: ' port2
	# while ! [[ $port2 =~ ^[0-9]+$ ]] || [ $port2 -gt 49151 ] || [ $port2 -eq $port ]
	# do
 	#   	echo "Error: Invalid Port"
 	#   	read -p 'The Port Where The SSH Server Should Run On: ' port2
 	# done
	echo [+] Creating directory /redpot/ssh
	mkdir -p /redpot/ssh
	sleep 1
	echo [+] Copying python script to /redpot/ssh
	cp services/ssh/fakessh.py /redpot/ssh
	cp -r services/ssh/keys/ /redpot/ssh
	sleep 1
	echo [+] Creating systemd file
	cp services/ssh/fakessh.service /etc/systemd/system
	systemctl daemon-reload
	sleep 1
	echo [+] Done
	echo -------------------------------------------------------------------
	echo ‎‎‎‎‎‎‎‎‎‎'                   'Configuring MySQL Database
	echo -------------------------------------------------------------------
	echo [+] Creating user admin...
	# To avoid errors
	sudo mysql --execute="DROP USER IF EXISTS admin;CREATE USER 'admin'@'%' IDENTIFIED BY 'admin';GRANT SELECT ON *.* TO 'admin'@'%';"
	sleep 1
	echo [+] Configuring file /etc/mysql/mysql.conf.d/mysqld.cnf
	sed -i '31s/.*/bind-address = 0.0.0.0/' /etc/mysql/mysql.conf.d/mysqld.cnf
	sleep 1
	echo [+] Restarting MySQL service...
	systemctl restart mysql.service
	echo [+] Populating MySQL Database...
	python3 services/mysql/mysql_junk.py
	echo [+] Done
	;;
esac