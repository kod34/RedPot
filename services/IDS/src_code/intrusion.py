import PacketStrings
from PacketStrings import *
import json
from datetime import datetime
import urllib.parse
from scapy.all import *
import requests
import os
# from urllib.request import urlopen

LOG = open("/redpot/logs/IDS/intrusions.log", "a")
LOG_CSV = open("/var/www/web_stats/csv_files/intrusions.csv", "a")

LOG_ports = open("/redpot/logs/IDS/ports.log", "a")
LOG_ports_CSV = open("/var/www/web_stats/csv_files/ports.csv", "a")

LOG_traffic = open("/redpot/logs/IDS/traffic.log", "a")
LOG_traffic_CSV = open("/var/www/web_stats/csv_files/traffic.csv", "a")

lease_dates = open("/redpot/logs/IDS/lease.log", "a")
locations = open("/redpot/logs/IDS/locations.csv", "a")

SQLinjections = json.loads(open('/redpot/IDS/src_code/attacks/SQLinjections.json').read())
XSSinjections = json.loads(open('/redpot/IDS/src_code/attacks/XSSinjections.json').read(), strict=False)

ip_dict = {}
ssh_dict = {}
fmt = '%Y-%m-%d %H:%M:%S'
tstamp1 = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), fmt)
ssh_tstamp1 = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), fmt)
port_list = [21, 22, 23, 25, 42, 53, 80, 88, 110, 119, 135, 137, 138, 138, 143, 443, 465, 993, 995, 1025, 3306]
k2 = datetime.strptime(datetime.now().strftime("2018-06-06 15:15:15"), fmt)

    #  Paid service
    #  try:
    #     url = 'http://ipinfo.io/'+ip+'/json'
    #     response = urlopen(url)
    #     data = json.load(response)
    #     country = data['country']
    # except:
    #     country = 'local'

#geolocation-db
def location1(ip_add):
    global country
    ip_add = PacketStrings.attacker_ip
    try: 
        response = requests.get("https://geolocation-db.com/json/"+ip_add+"&position=true").json()
        country = response['country_name']
    except:
        country = 'Error'
    finally:
        if(country == 'Not found'):
            country = 'local'


#geo plugin (120 per minute)
def location2(ip_add):
	global country
	ip_add = PacketStrings.attacker_ip
	try:
		response = requests.get("http://www.geoplugin.net/json.gp?ip="+ip_add).json()
		country = response['geoplugin_countryName']
	except:
		country = 'Error'
		print(response)
	finally:
		if(country == None):
			country = 'local'

def lease():
    global scan_dict
    if os.stat("/redpot/logs/IDS/lease.log").st_size == 0:
        locations = open("/redpot/logs/IDS/locations.csv", "w")
        reset_on = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), fmt)
        lease_dates.write("\n"+str(reset_on))
    else:
        with open('/redpot/logs/IDS/lease.log') as f:
            for line in f:
                pass
            last_line = datetime.strptime(line, fmt)
            time_now = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), fmt)
            lease_time = abs(time_now-last_line)
            lease_sec = int(round(lease_time.total_seconds()))
            if (lease_sec > 259200 ):
            	locations = open("/redpot/logs/IDS/locations.csv", "w")
            	reset_on = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), fmt)
            	lease_dates.write("\n"+str(reset_on))

def traffic():
    global country
    port = PacketStrings.target_port
    ip = PacketStrings.attacker_ip
    if(port != ''):
        LOG_traffic.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S")+" | Port "+str(port)+" is catching traffic from IP "+ip+"\r\r\n")
        LOG_traffic_CSV.write(datetime.now().strftime("%d-%m-%Y,%H:%M:%S")+","+str(port)+","+ip+"\n")

def Port_scanner():
    global scan_dict
    global country
    port = PacketStrings.target_port
    ip = PacketStrings.attacker_ip
    if(port in port_list):
    	loc_read = open("/redpot/logs/IDS/locations.csv", "r")
    	found = False
    	for row in loc_read:
    		if (ip == row.split(',')[0]):
    			country = row.split(',')[1]
    			LOG_ports.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S")+" | Port "+str(port)+" is targeted by IP "+ip+"\r\r\n")
    			LOG_ports_CSV.write(datetime.now().strftime("%d-%m-%Y,%H:%M:%S")+","+str(port)+","+ip+","+country+"\n")
    			found = True
    			break
    	if (not found):
    		location2(ip)
    		print(country)
    		loc_write = open("/redpot/logs/IDS/locations.csv", "a")
    		loc_write.write(ip+","+country+"\n")
    		loc_write.flush()
    		LOG_ports.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S")+" | Port "+str(port)+" is targeted by IP "+ip+"\r\r\n")
    		LOG_ports_CSV.write(datetime.now().strftime("%d-%m-%Y,%H:%M:%S")+","+str(port)+","+ip+","+country+"\n")

        
        
def SQLintrusion():
    global country
    global k2
    Port = PacketStrings.target_port
    ip_SQL = PacketStrings.attacker_ip
    sus = PacketStrings.tcp_payload
    k1 = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), fmt)
    diff = k1-k2
    diff_sec = int(round(diff.total_seconds()))
    if (len(sus) != 0 and conf.route.route("0.0.0.0")[2] != ip_SQL and (Port==80 or Port ==3306) and diff_sec > 2):
        for x in SQLinjections:
            if (urllib.parse.quote_plus(x) in sus):
                k2 = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), fmt)
                location1(ip_SQL)
                LOG.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S")+" | Possible Intrusion Detected | Type = SQLinjection | IP = "+ip_SQL+" | Payload = "+str(x)+"\r\r\n")
                LOG_CSV.write(datetime.now().strftime("%d-%m-%Y,%H:%M:%S")+",SQLinjection,"+ip_SQL+","+country+"\n")
                break

def XSSintrusion():
    global country
    global k2
    ip_XSS = PacketStrings.attacker_ip
    sus = PacketStrings.tcp_payload
    Port = PacketStrings.target_port
    k1 = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), fmt)
    diff = k1-k2
    diff_sec = int(round(diff.total_seconds()))
    if (len(sus) != 0 and conf.route.route("0.0.0.0")[2] != ip_XSS and (Port==80 or Port ==3306) and diff_sec > 2):
        for x in XSSinjections:
            if (urllib.parse.quote_plus(x) in sus):
                k2 = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), fmt)
                location1(ip_XSS)
                LOG.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S")+" | Possible Intrusion Detected | Type = XSS | IP = "+ip_XSS+" | Payload = "+str(x)+"\r\r\n")
                LOG_CSV.write(datetime.now().strftime("%d-%m-%Y,%H:%M:%S")+",XSS,"+ip_XSS+","+country+"\n")
                break


def SSH_Flood():
    global country
    global ssh_dict
    global ssh_tstamp1
    ssh_tstamp2 = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), fmt)
    ip = PacketStrings.attacker_ip
    port = PacketStrings.target_port
    if(port == 22):
	    if ip not in ssh_dict :
	        ssh_dict.update({ip: 0})
	    else:
	        ssh_dict[ip]+=1
	    ssh_td = ssh_tstamp2-ssh_tstamp1
	    ssh_td_sec = int(round(ssh_td.total_seconds()))
	    if (ssh_td_sec > 60):
	        ssh_key_list = list(ssh_dict.keys())
	        ssh_val_list = list(ssh_dict.values())
	        ssh_limit = 50
	        for x in ssh_val_list :
	            if (x > ssh_limit): 
	                ssh_ip_position = ssh_val_list.index(x)
	                ssh_ip = ssh_key_list[ssh_ip_position]
	                location1(ssh_ip)
	                LOG.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S")+" | Possible Intrusion Detected | Type = SSH BruteForce | IP = "+ssh_ip+"\r\r\n")
	                LOG_CSV.write(datetime.now().strftime("%d-%m-%Y,%H:%M:%S")+",SSH BruteForce,"+ssh_ip+","+country+"\n")
	        ssh__dict = {}
	        ssh_tstamp1 = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), fmt)

def Flood():
    global country
    global ip_dict
    global tstamp1
    tstamp2 = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), fmt)
    ip = PacketStrings.attacker_ip
    port = PacketStrings.target_port
    if(port != 22):
        if ip not in ip_dict :
            ip_dict.update({ip: 0})
        else:
            ip_dict[ip]+=1
        td = tstamp2-tstamp1
        td_sec = int(round(td.total_seconds()))
        if (td_sec > 60):
            key_list = list(ip_dict.keys())
            val_list = list(ip_dict.values())
            threshold = 600
            for x in val_list :
                if (x > threshold):
                    ip_position = val_list.index(x)
                    dos_ip = key_list[ip_position]
                    location1(dos_ip)
                    LOG.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S")+" | Possible Intrusion Detected | Type = Flood Attack | IP = "+dos_ip+"\r\r\n")
                    LOG_CSV.write(datetime.now().strftime("%d-%m-%Y,%H:%M:%S")+",TCP/UDP Flood,"+dos_ip+","+country+"\n")
            ip_dict = {}
            tstamp1 = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), fmt)
        

