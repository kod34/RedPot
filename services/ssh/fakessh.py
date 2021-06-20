#!/usr/bin/env python3
"""Fake SSH Server Utilizing Paramiko"""
import argparse
import threading
import socket
import sys
import traceback
import paramiko
import time
from datetime import datetime
import requests
# from urllib.request import urlopen


LOG = open("/redpot/logs/SSH/fakessh.log", "a")
LOG_CSV = open("/var/www/web_stats/csv_files/fakessh.csv", "a")
HOST_KEY = paramiko.RSAKey(filename='/redpot/ssh/keys/private.key')
SSH_BANNER = "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.1"


def handle_cmd(cmd, chan):
    """Branching statements to handle and prepare a response for a command"""
    response = ""
    if cmd.startswith("sudo"):
    	LOG.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S")+"  $ " + cmd + "\n")
    	LOG.flush()
    	response = "[sudo] password for www-data: "
    	chan.send(response)
    	time.sleep(500)

    elif cmd.startswith("ls"):
    	LOG.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S")+"  $ " + cmd + "\n")
    	LOG.flush()
    	response = "Desktop  Downloads  Pictures  Templates  Videos  Documents  Music  Public"
    	chan.send(response + "\r\n")


    elif cmd.startswith("pwd"):
    	LOG.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S")+"  $ " + cmd + "\n")
    	LOG.flush()
    	response = "/home/www-data"
    	chan.send(response + "\r\n")

    elif cmd.startswith("cd"):
    	LOG.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S")+"  $ " + cmd + "\n")
    	LOG.flush()
    	response = "cd: no such file or directory: "+cmd[2:]
    	chan.send(response + "\r\n")
    	return

    elif cmd.startswith("cat"):
    	LOG.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S")+"  $ " + cmd + "\n")
    	LOG.flush()
    	response = "cat: "+cmd[3:]+": No such file or directory"
    	chan.send(response + "\r\n")
    	return

    elif cmd.startswith("rm"):
    	LOG.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S")+"  $ " + cmd + "\n")
    	LOG.flush()
    	response = "rm: cannot remove '"+cmd[2:]+"': No such file or directory"
    	chan.send(response + "\r\n")
    	return

    elif cmd == "whoami":
    	LOG.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S")+"  $ " + cmd + "\n")
    	LOG.flush()
    	response = "www-data"
    	chan.send(response + "\r\n")
    	return

    else:
    	LOG.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S")+"  $ " + cmd + "\n")
    	LOG.flush()    
    	response = cmd+": command not found"
    	chan.send(response + "\r\n")
    	return

    


class FakeSshServer(paramiko.ServerInterface):
    """Settings for paramiko server interface"""
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if password == '123456789':
        	LOG.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S")+"  Password "+password+" attempted"+"\r\n")
        	LOG.flush()
        	return paramiko.AUTH_SUCCESSFUL
        else :
        	LOG.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S")+"  Password "+password+" attempted"+"\r\n")
        	LOG.flush()
        	time.sleep(3)
        	return "Permission denied, please try again."

    def get_allowed_auths(self, username):
        return 'password'

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True


def handle_connection(client, addr):
    """Handle a new ssh connection"""

    LOG.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S")+"  [!] Connection from " + addr[0] + "\n")
    
    # Payed service    
    # try:
    #     url = 'http://ipinfo.io/'+addr[0]+'/json'
    #     response = urlopen(url)
    #     data = json.load(response)
    #     country = data['country']
    # except:
    #     country = 'local'
    # finally:
    #     LOG_CSV.write(datetime.now().strftime("%d-%m-%Y,%H:%M:%S")+","+addr[0]+","+country+"\n")
    #     LOG_CSV.flush()

    #getlocation-db
    response = requests.get("https://geolocation-db.com/json/"+addr[0]+"&position=true").json()
    country = response['country_name']
    if(country == 'Not found'):
        country = 'local'
    LOG_CSV.write(datetime.now().strftime("%d-%m-%Y,%H:%M:%S")+","+addr[0]+","+country+"\n")
    LOG_CSV.flush()

        
    try:
        transport = paramiko.Transport(client)
        transport.add_server_key(HOST_KEY)
        # Change banner to appear legit on nmap (or other network) scans
        transport.local_version = SSH_BANNER
        server = FakeSshServer()
        try:
            transport.start_server(server=server)
        except paramiko.SSHException:
            raise Exception("SSH negotiation failed")
        # wait for auth
        chan = transport.accept(20)
        if chan is None:
            raise Exception("No channel")

        server.event.wait(10)
        if not server.event.is_set():
            raise Exception("No shell request")

        try:
            chan.send("\r\n")
            run = True
            while run:
                chan.send("$ ")
                command = ""
                while not command.endswith("\r"):
                    transport = chan.recv(1024)
                    # Echo input to psuedo-simulate a basic terminal
                    chan.send(transport)
                    command += transport.decode("utf-8")

                chan.send("\r\n")
                command = command.rstrip()
                if command == "exit":
                    LOG.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S")+"  Connection from " + addr[0] + " closed.\n")
                    LOG.flush()
                    run = False
                else:
                    handle_cmd(command, chan)

        except Exception as err:
            traceback.print_exc()
            try:
                transport.close()
            except Exception:
                pass

        chan.close()

    except Exception as err:
        traceback.print_exc()
        try:
            transport.close()
        except Exception:
            pass


def start_server(port, bind):
    """Init and run the ssh server"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((bind, port))
    except Exception as err:
        traceback.print_exc()
        sys.exit(1)

    threads = []
    while True:
        try:
            sock.listen(100)
            client, addr = sock.accept()
        except Exception as err:
            traceback.print_exc()
        new_thread = threading.Thread(target=handle_connection, args=(client, addr))
        new_thread.start()
        threads.append(new_thread)

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run a fake ssh server')
    parser.add_argument("--port", "-p", help="The port to bind the ssh server to (default 22)", default=22, type=int, action="store")
    parser.add_argument("--bind", "-b", help="The address to bind the ssh server to", default="", type=str, action="store")
    args = parser.parse_args()
    start_server(args.port, args.bind)
