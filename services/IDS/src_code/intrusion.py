import PacketStrings
from PacketStrings import *
import json
from datetime import datetime
import urllib.parse
from scapy.all import *

SQLinjections = json.loads(open('/redpot/IDS/src_code/attacks/SQLinjections.json').read())
XSSinjections = json.loads(open('/redpot/IDS/src_code/attacks/XSSinjections.json').read(), strict=False)

LOG = open("/redpot/logs/IDS/intrusions.log", "a")
LOG_ports = open("/redpot/logs/IDS/ports.log", "a")
LOG_CSV = open("/var/www/web_stats/csv_files/intrusions.csv", "a")
LOG_ports_CSV = open("/var/www/web_stats/csv_files/ports.csv", "a")
old_ip = ""
old_load = ""

def SQLintrusion(pkt):
    global old_ip
    global old_load
    ip = PacketStrings.attacker_ip
    sus = PacketStrings.tcp_payload
    new_ip = ip
    if (len(sus) != 0):
        for x in SQLinjections:
            if ((old_ip != new_ip or old_load != x) and conf.route.route("0.0.0.0")[2] != ip and urllib.parse.quote_plus(x) in sus):
                LOG.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S")+" | Possible Intrusion Detected | Type = SQLinjection | IP = "+ip+" | Payload = "+str(x)+"\r\r\n")
                LOG.flush()
                try:
                    response = requests.get("https://geolocation-db.com/json/"+ip+"&position=true").json()
                    country = response['country_name']
                except:
                    country = 'local'
                finally:
                    LOG_CSV.write(datetime.now().strftime("%d-%m-%Y,%H:%M:%S")+",SQLinjection,"+ip+","+country+"\n")
                    LOG_CSV.flush()
                    old_ip = ip
                    old_load = x



def XSSintrusion(pkt):
    global old_ip
    global old_load
    ip = PacketStrings.attacker_ip
    sus = PacketStrings.tcp_payload
    new_ip = ip
    if (len(sus) != 0):
        for x in XSSinjections:
            if ((old_ip != new_ip or old_load != x) and conf.route.route("0.0.0.0")[2] != ip and urllib.parse.quote_plus(x) in sus):
                LOG.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S")+" | Possible Intrusion Detected | Type = XSS | IP = "+ip+" | Payload = "+str(x)+"\r\r\n")
                LOG.flush()
                try:
                    response = requests.get("https://geolocation-db.com/json/"+ip+"&position=true").json()
                    country = response['country_name']
                except:
                    country = 'local'
                finally:
                    LOG_CSV.write(datetime.now().strftime("%d-%m-%Y,%H:%M:%S")+",XSS,"+ip+","+country+"\n")
                    LOG_CSV.flush()
                    old_ip = ip
                    old_load = x


def Port_scanner(pkt):
    port = PacketStrings.target_port
    ip = PacketStrings.attacker_ip
    if(port != ''):
        try:
            response = requests.get("https://geolocation-db.com/json/"+ip+"&position=true").json()
            country = response['country_name']
        except:
            country = 'local'
        finally:
            LOG_ports.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S")+" | Port "+str(port)+" is catching traffic from IP "+ip+"\r\r\n")
            LOG_ports_CSV.write(datetime.now().strftime("%d-%m-%Y,%H:%M:%S")+","+str(port)+","+ip+","+country+"\n")
            LOG_ports.flush()
            LOG_ports_CSV.flush()