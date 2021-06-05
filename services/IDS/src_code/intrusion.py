import PacketStrings
from PacketStrings import packetString
import json
from datetime import datetime
import logging
import urllib.parse
from scapy.all import *

SQLinjections = json.loads(open('/redpot/IDS/src_code/attacks/SQLinjections.json').read())
XSSinjections = json.loads(open('/redpot/IDS/src_code/attacks/XSSinjections.json').read(), strict=False)

LOG = open("/redpot/logs/IDS/intrusions.log", "a")
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
                old_ip = ip
                old_load = x
