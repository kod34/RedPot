import PacketStrings
from PacketStrings import *
import json
from datetime import datetime
import urllib.parse
from scapy.all import *
import requests

SQLinjections = json.loads(open('/redpot/IDS/src_code/attacks/SQLinjections.json').read())
XSSinjections = json.loads(open('/redpot/IDS/src_code/attacks/XSSinjections.json').read(), strict=False)

LOG = open("/redpot/logs/IDS/intrusions.log", "a")
LOG_ports = open("/redpot/logs/IDS/ports.log", "a")
LOG_CSV = open("/var/www/web_stats/csv_files/intrusions.csv", "a")
LOG_ports_CSV = open("/var/www/web_stats/csv_files/ports.csv", "a")
old_ip = ""
old_load = ""
ip_dict = {}
fmt = '%Y-%m-%d %H:%M:%S'
tstamp1 = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), fmt)
country = ''


def location():
    global country
    ip = PacketStrings.attacker_ip
    try:
         response = requests.get("https://geolocation-db.com/json/"+ip+"&position=true").json()
         country = response['country_name']
    except:
        country = 'local'
    finally:
        if(country == 'Not found'):
            country = 'local'

def Port_scanner(pkt):
    global country
    port = PacketStrings.target_port
    ip_port = PacketStrings.attacker_ip
    if(port != ''):
        LOG_ports.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S")+" | Port "+str(port)+" is catching traffic from IP "+ip_port+"\r\r\n")
        LOG_ports_CSV.write(datetime.now().strftime("%d-%m-%Y,%H:%M:%S")+","+str(port)+","+ip_port+","+country+"\n")
            
def SQLintrusion(pkt):
    global old_ip
    global old_load
    ip_SQL = PacketStrings.attacker_ip
    sus = PacketStrings.tcp_payload
    new_ip = ip_SQL
    if (len(sus) != 0):
        for x in SQLinjections:
            if ((old_ip != new_ip or old_load != x) and conf.route.route("0.0.0.0")[2] != ip_SQL and urllib.parse.quote_plus(x) in sus):
                LOG.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S")+" | Possible Intrusion Detected | Type = SQLinjection | IP = "+ip_SQL+" | Payload = "+str(x)+"\r\r\n")
                LOG_CSV.write(datetime.now().strftime("%d-%m-%Y,%H:%M:%S")+",SQLinjection,"+ip_SQL+","+country+"\n")
                old_ip = ip_SQL
                old_load = x



def XSSintrusion(pkt):
    global old_ip
    global old_load
    ip_XSS = PacketStrings.attacker_ip
    sus = PacketStrings.tcp_payload
    new_ip = ip_XSS
    if (len(sus) != 0):
        for x in XSSinjections:
            if ((old_ip != new_ip or old_load != x) and conf.route.route("0.0.0.0")[2] != ip_XSS and urllib.parse.quote_plus(x) in sus):
                LOG.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S")+" | Possible Intrusion Detected | Type = XSS | IP = "+ip_XSS+" | Payload = "+str(x)+"\r\r\n")
                LOG_CSV.write(datetime.now().strftime("%d-%m-%Y,%H:%M:%S")+",XSS,"+ip_XSS+","+country+"\n")
                old_ip = ip_XSS
                old_load = x

def Flood(pkt):
    global ip_dict
    global tstamp1
    tstamp2 = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), fmt)
    ip = PacketStrings.attacker_ip
    if ip not in ip_dict :
        ip_dict.update({str(ip): 0})
    else:
        ip_dict[ip]+=1
    td = tstamp2-tstamp1
    td_sec = int(round(td.total_seconds()))
    if (td_sec > 60):
        key_list = list(ip_dict.keys())
        val_list = list(ip_dict.values())
        threshold = 2500
        for x in val_list :
            if (x > threshold): 
                ip_position = val_list.index(x)
                dos_ip = key_list[ip_position]
                LOG.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S")+" | Possible Intrusion Detected | Type = Flood Attack | IP = "+dos_ip+"\r\r\n")
                LOG_CSV.write(datetime.now().strftime("%d-%m-%Y,%H:%M:%S")+",TCP/UDP Flood,"+dos_ip+","+country+"\n")

        ip_dict = {}
        tstamp1 = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), fmt)
        
        
