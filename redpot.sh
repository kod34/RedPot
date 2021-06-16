#!/bin/bash
set -e
if [[ $EUID -ne 0 ]];then
        echo "[!] Must be run as Root"
        exit 1
fi
echo -------------------------------------------------------------------
echo ‎‎‎‎'                    'Starting the SSH HoneyPot
echo -------------------------------------------------------------------
echo [+] Stopping SSH server
sleep 1
echo [+] Starting Fake-SSH Honeypot...
systemctl start fakessh
sleep 1
echo [+] Done
echo [*] You can view logs at: /redpot/logs/SSH/fakessh.log
echo -------------------------------------------------------------------
echo ‎‎‎‎'                      'Starting the RedPot IDS
echo -------------------------------------------------------------------
read -p 'Minimum Packet rate (Packets per minute) to be detected as a flood Attack: ' prate
sed -i "100s/threshold.*/threshold = $prate/" /redpot/IDS/src_code/intrusion.py
sleep 1
echo [+] Starting redpot_ids service...
systemctl start redpot_ids
sleep 1
echo [+] Done
echo [*] You can view Packet logs at: /redpot/logs/IDS/Redpot_ids.log
echo [*] You can view Intrusion logs at: /redpot/logs/IDS/intrusions.logs
