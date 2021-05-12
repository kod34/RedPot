#!/bin/bash
set -e
if [[ $EUID -ne 0 ]];then
        echo "[!] Must be run as Root"
        exit 1
fi
echo -------------------------------------------------------------------
echo ‎‎‎‎'                     'Starting SSH HoneyPot
echo -------------------------------------------------------------------
echo [+] Stopping SSH server
sleep 1
echo [+] Starting Fake-SSH Honeypot...
systemctl start fakessh
sleep 1
echo [+] Done
echo [*] You can view logs at: /redpot/logs/fakessh.log
