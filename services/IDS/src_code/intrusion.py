import PacketStrings
from PacketStrings import *
import json
from datetime import datetime
import urllib.parse
from scapy.all import *
import requests
import os
from netaddr import *
# from urllib.request import urlopen

LOG = open("/redpot/logs/IDS/intrusions.log", "a")

LOG_ports = open("/redpot/logs/IDS/ports.log", "a")

LOG_traffic = open("/redpot/logs/IDS/traffic.log", "a")

lease_dates = open("/redpot/logs/IDS/lease.log", "a")
locations = open("/redpot/logs/IDS/locations.csv", "a")

SQLinjections = json.loads(open('/redpot/IDS/src_code/attacks/SQLinjections.json').read())
XSSinjections = json.loads(open('/redpot/IDS/src_code/attacks/XSSinjections.json').read(), strict=False)

ip_dict = {}
ssh_dict = {}
sql_dict = {}
fmt = '%Y-%m-%d %H:%M:%S'
tstamp1 = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), fmt)
ssh_tstamp1 = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), fmt)
sql_tstamp1 = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), fmt)
port_list = [21, 22, 23, 25, 42, 53, 80, 88, 110, 119, 135, 137, 138, 138, 143, 443, 465, 993, 995, 1025, 3306]
k2 = datetime.strptime(datetime.now().strftime("2018-06-06 15:15:15"), fmt)

#  Ipinfo sucks
#  try:
#     url = 'http://ipinfo.io/'+ip+'/json'
#     response = urlopen(url)
#     data = json.load(response)
#     country = data['country']
# except:
#     country = 'local'

#geolocation-db sucks
# def location1(ip_add):
#     global country
#     ip_add = PacketStrings.attacker_ip
#     try: 
#         response = requests.get("https://geolocation-db.com/json/"+ip_add+"&position=true").json()
#         country = response['country_name']
#     except:
#         country = 'Error'
#     finally:
#         if(country == 'Not found'):
#             country = 'local'


#geo plugin (120 per minute)
def location2(ip_add):
    global country
    ip_add = PacketStrings.attacker_ip
    if (IPAddress(ip_add).is_private()):
        country = 'local'
    else:
        try:
            response = requests.get("http://www.geoplugin.net/json.gp?ip="+ip_add).json()
            country = response['geoplugin_countryName']
        except:
            country = 'Error'
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

def get_country(ip):
    global country
    loc_read = open("/redpot/logs/IDS/locations.csv", "r")
    found = False
    for row in loc_read:
        if (ip == row.split(',')[0]):
            found = True
            country = row.split(',')[1]
            break
    if(not found):
        location2(ip)
        loc_write = open("/redpot/logs/IDS/locations.csv", "a")
        loc_write.write(ip+","+country+"\n")
        loc_write.flush()

def traffic():
    port = PacketStrings.target_port
    ip = PacketStrings.attacker_ip
    if(port != '' and not IPAddress(ip).is_private()):
        LOG_traffic.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S")+" | Port "+str(port)+" is catching traffic from IP "+ip+"\r\r\n")
        with open("/var/www/web_stats/csv_files/traffic.csv", "a") as LOG_traffic_CSV:
            LOG_traffic_CSV.write((datetime.now().strftime("%d-%m-%Y,%H:%M:%S")+","+str(port)+","+ip).replace('\n', '')+"\n")
            LOG_traffic_CSV.flush()


def Port_scanner():
    global scan_dict
    global country
    port = PacketStrings.target_port
    ip_port = PacketStrings.attacker_ip
    if(port in port_list):
        get_country(ip_port)
        LOG_ports.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S")+" | Port "+str(port)+" is targeted by IP "+ip_port+"\r\r\n")
        with open("/var/www/web_stats/csv_files/ports.csv", "a") as LOG_ports_CSV:
            LOG_ports_CSV.write((datetime.now().strftime("%d-%m-%Y,%H:%M:%S")+","+str(port)+","+ip_port+","+country).replace('\n', '')+"\n")
            LOG_ports_CSV.flush()



def SQLintrusion():
    global country
    global k2
    Port = PacketStrings.target_port
    ip_SQL = PacketStrings.attacker_ip
    get_country(ip_SQL)
    sus = PacketStrings.tcp_payload
    k1 = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), fmt)
    diff = k1-k2
    diff_sec = int(round(diff.total_seconds()))
    if (len(sus) != 0 and conf.route.route("0.0.0.0")[2] != ip_SQL and (Port==80 or Port ==3306) and diff_sec > 2):
        for x in SQLinjections:
            if (urllib.parse.quote_plus(x) in sus):
                k2 = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), fmt)
                LOG.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S")+" | Possible Intrusion Detected | Type = SQLinjection | IP = "+ip_SQL+" | Payload = "+str(x)+"\r\r\n")
                with open("/var/www/web_stats/csv_files/intrusions.csv", "a") as LOG_CSV:
                    LOG_CSV.write((datetime.now().strftime("%d-%m-%Y,%H:%M:%S")+",SQLinjection,"+ip_SQL+","+country).replace('\n', '')+"\n")
                    LOG_CSV.flush()
                break

def XSSintrusion():
    global country
    global k2
    ip_XSS = PacketStrings.attacker_ip
    get_country(ip_XSS)
    sus = PacketStrings.tcp_payload
    Port = PacketStrings.target_port
    k1 = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), fmt)
    diff = k1-k2
    diff_sec = int(round(diff.total_seconds()))
    if (len(sus) != 0 and conf.route.route("0.0.0.0")[2] != ip_XSS and (Port==80 or Port ==3306) and diff_sec > 2):
        for x in XSSinjections:
            if (urllib.parse.quote_plus(x) in sus):
                k2 = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), fmt)
                LOG.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S")+" | Possible Intrusion Detected | Type = XSS | IP = "+ip_XSS+" | Payload = "+str(x)+"\r\r\n")
                with open("/var/www/web_stats/csv_files/intrusions.csv", "a") as LOG_CSV:
                    LOG_CSV.write((datetime.now().strftime("%d-%m-%Y,%H:%M:%S")+",XSS,"+ip_XSS+","+country).replace('\n', '')+"\n")
                    LOG_CSV.flush()
                break


def SSH_Flood():
    global country
    global ssh_dict
    global ssh_tstamp1
    ssh_tstamp2 = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), fmt)
    ip = PacketStrings.attacker_ip
    get_country(ip)
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
            ssh_limit = 240
            for x in ssh_val_list :
                if (x > ssh_limit): 
                    ssh_ip_position = ssh_val_list.index(x)
                    ssh_ip = ssh_key_list[ssh_ip_position]
                    LOG.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S")+" | Possible Intrusion Detected | Type = SSH BruteForce | IP = "+ssh_ip+"\r\r\n")
                    with open("/var/www/web_stats/csv_files/intrusions.csv", "a") as LOG_CSV:
                        LOG_CSV.write((datetime.now().strftime("%d-%m-%Y,%H:%M:%S")+",SSH BruteForce,"+ssh_ip+","+country).replace('\n', '')+"\n")
                        LOG_CSV.flush()
            ssh__dict = {}
            ssh_tstamp1 = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), fmt)

def Flood():
    global country
    global ip_dict
    global tstamp1
    tstamp2 = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), fmt)
    ip = PacketStrings.attacker_ip
    get_country(ip)
    port = PacketStrings.target_port
    if(port != 22 and port != 3306):
        if ip not in ip_dict :
            ip_dict.update({ip: 0})
        else:
            ip_dict[ip]+=1
        td = tstamp2-tstamp1
        td_sec = int(round(td.total_seconds()))
        if (td_sec > 60):
            key_list = list(ip_dict.keys())
            val_list = list(ip_dict.values())
            threshold = 400
            for x in val_list :
                if (x > threshold):
                    ip_position = val_list.index(x)
                    dos_ip = key_list[ip_position]
                    LOG.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S")+" | Possible Intrusion Detected | Type = Flood Attack | IP = "+dos_ip+"\r\r\n")
                    with open("/var/www/web_stats/csv_files/intrusions.csv", "a") as LOG_CSV:
                        LOG_CSV.write((datetime.now().strftime("%d-%m-%Y,%H:%M:%S")+",TCP/UDP Flood,"+dos_ip+","+country).replace('\n', '')+"\n")
                        LOG_CSV.flush()
            ip_dict = {}
            tstamp1 = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), fmt)


def SQL_Flood():
    global country
    global sql_dict
    global sql_tstamp1
    sql_tstamp2 = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), fmt)
    ip = PacketStrings.attacker_ip
    get_country(ip)
    port = PacketStrings.target_port
    if(port == 3306):
        if ip not in sql_dict :
            sql_dict.update({ip: 0})
        else:
            sql_dict[ip]+=1
        sql_td = sql_tstamp2-sql_tstamp1
        sql_td_sec = int(round(sql_td.total_seconds()))
        if (sql_td_sec > 60):
            sql_key_list = list(sql_dict.keys())
            sql_val_list = list(sql_dict.values())
            sql_limit = 100
            for x in sql_val_list :
                if (x > sql_limit): 
                    sql_ip_position = sql_val_list.index(x)
                    sql_ip = sql_key_list[sql_ip_position]
                    LOG.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S")+" | Possible Intrusion Detected | Type = SQL BruteForce | IP = "+sql_ip+"\r\r\n")
                    with open("/var/www/web_stats/csv_files/intrusions.csv", "a") as LOG_CSV:
                        LOG_CSV.write((datetime.now().strftime("%d-%m-%Y,%H:%M:%S")+",SQL BruteForce,"+sql_ip+","+country).replace('\n', '')+"\n")
                        LOG_CSV.flush()
            sql__dict = {}
            sql_tstamp1 = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), fmt)