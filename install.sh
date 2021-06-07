#!/bin/bash
set -e
if [[ $EUID -ne 0 ]];then
        echo "[!] Must be run as Root"
        exit 1
fi
echo -------------------------------------------------------------------
echo ‎‎‎‎‎‎‎‎‎‎'                       'Updating Packages
echo -------------------------------------------------------------------
apt update
echo -------------------------------------------------------------------
echo ‎‎‎‎'                      'Installing Python3
echo -------------------------------------------------------------------
apt -y install python3
echo -------------------------------------------------------------------
echo ‎‎‎‎'                        'Installing pip3
echo -------------------------------------------------------------------
apt -y install python3-pip
echo -------------------------------------------------------------------
echo ‎‎‎‎'                       'Installing Apache
echo -------------------------------------------------------------------
apt -y install apache2
apt -y install php php-cli php-fpm php-json php-common php-mysql php-zip php-gd php-mbstring php-curl php-xml php-pear php-bcmath
echo -------------------------------------------------------------------
echo ‎‎‎‎'                 'Installing MySQL & Dependencies
echo -------------------------------------------------------------------
apt install mysql-server -y
echo [+] Installing required Python packages...
sleep 1
python3 -m pip install mysql-connector-python
pip3 install -r requirements.txt
echo [+] Done
echo -------------------------------------------------------------------
echo ‎‎‎‎'                 'Installing ELK & Dependencies
echo -------------------------------------------------------------------
echo [+] Installing Java...
apt -y install openjdk-8-jdk
echo [+] Installing Elasticsearch...
wget -P /opt https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.13.1-amd64.deb
dpkg -i /opt/elasticsearch-7.13.1-amd64.deb
echo [+] Installing Kibana...
wget -P /opt https://artifacts.elastic.co/downloads/kibana/kibana-7.13.1-amd64.deb
dpkg -i /opt/kibana-7.13.1-amd64.deb
echo [+] Installing Logstash...
apt -y install apt-transport-https
wget -P /opt https://artifacts.elastic.co/downloads/logstash/logstash-7.13.1-amd64.deb
dpkg -i /opt/logstash-7.13.1-amd64.deb
echo [+] Installing Filebeat...
wget -P /opt https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-7.13.1-amd64.deb
dpkg -i /opt/filebeat-7.13.1-amd64.deb