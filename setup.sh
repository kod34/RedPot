#!/bin/bash
set -e
if [[ $EUID -ne 0 ]];then
	echo "[!] The Script must be run as Root!"
	exit 1
fi
echo -e "\033[31mSetting up the vulnerable environment might cause you to lose sensitive data\033[0m"
sleep 1
read -p 'Do you wish to continue?(Y/N) ' continue
echo
case $continue in 
	n|N|No|no|No)
	echo -e '\033[31mExiting...\033[0m'
	sleep 1
	exit 1
	;;

	y|Y|yes|Yes|YES)
	echo -------------------------------------------------------------------
	echo ‎‎‎‎'                    'Configuring the environment
	echo -------------------------------------------------------------------
	echo [+] Creating directory /redpot
	rm -rf /redpot
	mkdir -p /redpot
	sleep 1
	echo [+] Creating log directories in /redpot/logs
	mkdir -p /redpot/logs/SSH
	mkdir -p /redpot/logs/IDS
	sleep 1
	echo [+] Done
	echo -------------------------------------------------------------------
	echo ‎‎‎‎‎‎‎‎‎‎'                     'Configuring the Web server
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
	echo 1 : Bootstrap-shop
	echo 2 : Digishop-mini
	echo 3 : Pomato-shop
	echo 4 : Electronix
	echo 5 : Tool-shop
	echo
	read -p "Which template would you like to use? " template
	sleep 1
	case $template in
		1|Bootstrap-shop)
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
		echo [+] Done
		echo [*] Fake website url: http://bootstrap-shop.com
		;;
		2|Digishop-mini)
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
		echo [+] Done
		echo [*] Fake website url: http://digishop-mini.com
		;;
		3|Pomato-shop)
		echo [+] Creating directory /redpot/apache
		mkdir -p /redpot/apache
		sleep 1
		echo [+] Downloading website files...
		wget -P /redpot/apache https://www.free-css.com/assets/files/free-css-templates/download/page262/pomato.zip
		echo [+] Extracting files...
		unzip /redpot/apache/pomato.zip -d /redpot/apache/
		echo [+] Copying files to /var/www/html
		cp -r /redpot/apache/pomato/* /var/www/html/
		sleep 1
		# echo [+] Configuring Ports...
		# sed -i '5s/.*/Listen '$port'/' /etc/apache2/ports.conf
		# sed -i '1s/.*/<VirtualHost *:'$port'>/' /etc/apache2/sites-available/000-default.conf
		# sleep 1
		echo [+] Configuring hostnames file /etc/hosts... 
		echo "127.0.0.1 pomato-shop.com www.pomato-shop.com" >> /etc/hosts
		sleep 1
		echo [+] Done
		echo [*] Fake website url: http://pomato-shop.com
		;;
		4|Electronix)
		echo [+] Creating directory /redpot/apache
		mkdir -p /redpot/apache
		sleep 1
		echo [+] Downloading website files...
		wget -P /redpot/apache https://www.free-css.com/assets/files/free-css-templates/download/page87/electronix.zip
		echo [+] Extracting files...
		unzip /redpot/apache/electronix.zip -d /redpot/apache/
		echo [+] Copying files to /var/www/html
		cp -r /redpot/apache/electronix/* /var/www/html/
		sleep 1
		# echo [+] Configuring Ports...
		# sed -i '5s/.*/Listen '$port'/' /etc/apache2/ports.conf
		# sed -i '1s/.*/<VirtualHost *:'$port'>/' /etc/apache2/sites-available/000-default.conf
		# sleep 1
		echo [+] Configuring hostnames file /etc/hosts... 
		echo "127.0.0.1 electronix-shop.com www.electronix-shop.com" >> /etc/hosts
		sleep 1
		echo [+] Done
		echo [*] Fake website url: http://electronix-shop.com
		;;
		5|Tool-shop)
		echo [+] Creating directory /redpot/apache
		mkdir -p /redpot/apache
		sleep 1
		echo [+] Downloading website files...
		wget -P /redpot/apache https://www.free-css.com/assets/files/free-css-templates/download/page88/tool-shop.zip
		echo [+] Extracting files...
		unzip /redpot/apache/tool-shop.zip -d /redpot/apache/
		echo [+] Copying files to /var/www/html
		cp -r /redpot/apache/tool-shop/* /var/www/html/
		sleep 1
		# echo [+] Configuring Ports...
		# sed -i '5s/.*/Listen '$port'/' /etc/apache2/ports.conf
		# sed -i '1s/.*/<VirtualHost *:'$port'>/' /etc/apache2/sites-available/000-default.conf
		# sleep 1
		echo [+] Configuring hostnames file /etc/hosts... 
		echo "127.0.0.1 tool-shop.ma www.tool-shop.ma" >> /etc/hosts
		sleep 1
		echo [+] Done
		echo [*] Fake website url: http://tool-shop.ma
		;;
		*)
		echo [-] Unknown Option
		echo [-] Exiting...
		sleep 1
		exit 1
		;;
	esac
	echo -------------------------------------------------------------------
	echo ‎‎‎‎'                    'Configuring the SSH server
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
	echo [+] Copying relevant files to /redpot/ssh
	cp services/ssh/fakessh.py /redpot/ssh
	cp -r services/ssh/keys/ /redpot/ssh
	sleep 1
	echo [+] Creating systemd file
	cp services/ssh/fakessh.service /etc/systemd/system
	systemctl daemon-reload
	sleep 1
	echo [+] Done
	echo -------------------------------------------------------------------
	echo ‎‎‎‎‎‎‎‎‎‎'                   'Configuring the MySql database
	echo -------------------------------------------------------------------
	echo [+] Starting MySQL service...
	sleep 1
	systemctl start mysql
	echo [+] Creating user "'"'admin'"'"...
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
	echo -------------------------------------------------------------------
	echo ‎‎‎‎‎‎‎‎‎‎'                      'Configuring the IDS
	echo -------------------------------------------------------------------
	echo [+] Creating directory /redpot/IDS
	mkdir -p /redpot/IDS
	sleep 1
	echo [+] Copying relevant files to /redpot/IDS
	cp -r services/IDS/src_code /redpot/IDS
	sleep 1
	echo [+] Creating systemd file
	cp services/IDS/redpot_ids.service /etc/systemd/system
	systemctl daemon-reload
	sleep 1
	echo [+] Done
	echo -------------------------------------------------------------------
	echo ‎‎‎‎‎‎‎‎‎‎'                 'Configuring the Stats website
	echo -------------------------------------------------------------------
	echo [+] Setting up Admin Credentials...
	read -p 'Username: ' admin
	read -s -p 'Password: ' pass
	htpasswd -cb /etc/apache2/htpasswd.users $admin $pass
	echo [*] 'Admin credentials are stored in /etc/apache2/htpasswd.users'
	sleep 2
	echo [+] Configuring the Web page on Port 5001...
	cp services/stats/web_stats.conf /etc/apache2/sites-available
	cp -r services/stats/web_stats /var/www
	sed -i '6s/.*/Listen 5001/' /etc/apache2/ports.conf
	mkdir -p /var/www/web_stats/csv_files
	a2ensite web_stats.conf
	sleep 1
	echo [+] Starting the Apache server...
	systemctl restart apache2
	echo [+] Done
	echo [*] You can view real-time intrusion statistics at: http://localhost:5001
	;;
esac
