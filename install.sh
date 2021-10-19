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
echo ‎‎‎‎'                 'Installing MySQL and Dependencies
echo -------------------------------------------------------------------
apt install mysql-server -y
echo [+] Installing required Python packages...
sleep 1
python3 -m pip install mysql-connector-python
pip3 install -r requirements.txt
echo [+] Done