#!/bin/bash
set -e
if [[ $EUID -ne 0 ]];then
        echo "[!] Must be run as Root"
        exit 1
fi
echo -------------------------------------------------------------------
echo ‎‎‎‎'                    'Starting the Apache Server
echo -------------------------------------------------------------------
systemctl restart apache2
sleep 1
echo [+] Done
echo -------------------------------------------------------------------
echo ‎‎‎‎'                    'Starting the MySql Server
echo -------------------------------------------------------------------
systemctl restart mysql.service
sleep 1
echo [+] Done
echo -------------------------------------------------------------------
echo ‎‎‎‎'                    'Starting the SSH HoneyPot
echo -------------------------------------------------------------------
echo [+] Stopping SSH server
sleep 1
read -p 'Enter a parameter to be used as an SSH password: ' sshp
sed -i "s/password == .*/password == '$sshp':/" /redpot/ssh/fakessh.py
sleep 1
echo [+] Starting Fake-SSH Honeypot...
systemctl restart fakessh
sleep 1
echo [+] Done
echo [*] Log Files: /redpot/logs/SSH/
echo -------------------------------------------------------------------
echo ‎‎‎‎'                      'Starting the RedPot IDS
echo -------------------------------------------------------------------
read -p 'Minimum Packet rate (Packets per minute) to be detected as a flood Attack: ' prate
while ! [[ $prate =~ ^[0-9]+$ ]]
do
        echo "Error: Invalid Input"
        read -p 'Minimum Packet rate (Packets per minute) to be detected as a flood Attack: ' prate
done        
sed -i "s/threshold =.*/threshold = $prate/" /redpot/IDS/src_code/intrusion.py
sleep 1
echo [+] Starting redpot_ids service...
systemctl restart redpot_ids
sleep 1
echo [+] Done
echo [*] Log Files: /redpot/logs/IDS/
