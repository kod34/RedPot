import re
from scapy.all import *

from Utils import *


RED = '\033[91m'
ENDC = '\033[0m'
URG = 0x20

attacker_ip = ''
tcp_payload = ''
target_port = ''

def ipString(ip):

    out = "[IP HEADER]" + "\n"
    out += "\t Version: " + str(ip.version) + "\n"
    out += "\t IHL: " + str(ip.ihl * 4) + " bytes" + "\n"
    out += "\t ToS: " + str(ip.tos) + "\n"
    out += "\t Total Length: " + str(ip.len) + "\n"
    out += "\t Identification: " + str(ip.id) + "\n"
    out += "\t Flags: " + str(ip.flags) + "\n"
    out += "\t Fragment Offset: " + str(ip.frag) + "\n"
    out += "\t TTL: " + str(ip.ttl) + "\n"
    out += "\t Protocol: " + str(ip.proto) + "\n"
    out += "\t Header Checksum: " + str(ip.chksum) + "\n"
    out += "\t Source: " + str(ip.src) + "\n"
    out += "\t Destination: " + str(ip.dst) + "\n"
    if (ip.ihl > 5):
        out += "\t Options: " + str(ip.options) + "\n"
    return out


def tcpString(tcp):

        out = "[TCP Header]" + "\n"
        out += "\t Source Port: " + str(tcp.sport) + "\n"
        out += "\t Destination Port: " + str(tcp.dport) + "\n"
        out += "\t Sequence Number: " + str(tcp.seq) + "\n"
        out += "\t Acknowledgment Number: " + str(tcp.ack) + "\n"
        out += "\t Data Offset: " + str(tcp.dataofs) + "\n"
        out += "\t Reserved: " + str(tcp.reserved) + "\n"
        out += "\t Flags: " + tcp.underlayer.sprintf("%TCP.flags%") + "\n"
        out += "\t Window Size: " + str(tcp.window) + "\n"
        out += "\t Checksum: " + str(tcp.chksum) + "\n"
        if (tcp.flags & URG):
            out += "\t Urgent Pointer: " + str(tcp.window) + "\n"
        if (tcp.dataofs > 5):
            out += "\t Options: " + str(tcp.options) + "\n"
        return out


def udpString(udp):

    out = "[UDP Header]" + "\n"
    out += "\t Source Port: " + str(udp.sport) + "\n"
    out += "\t Destination Port: " + str(udp.dport) + "\n"
    out += "\t Length: " + str(udp.len) + "\n"
    out += "\t Checksum: " + str(udp.chksum) + "\n"
    return out


def payloadString(pkt):
    if (pkt.payload):
        data = str(pkt.payload)
        lines = data.splitlines()
        s = ""
        for line in lines:
            s += "\t" + line + "\n"
        out = s
        return out
    else:
        return ""


def packetString(pkt):
    global attacker_ip
    global tcp_payload
    global target_port

    out = ""
    if (IP in pkt):
        attacker_ip = pkt[IP].src
        out += ipString(pkt[IP])
    elif (IPv6 in pkt):
        # TODO
        pass
    if (TCP in pkt):
        tcp_payload = payloadString(pkt[TCP])
        target_port = pkt[TCP].dport
        out += tcpString(pkt[TCP])
        out += "[TCP Payload]" + "\n"
        out+= payloadString(pkt[TCP])
    elif (UDP in pkt):
        target_port = pkt[UDP].dport
        out += udpString(pkt[UDP])
        out += "[UDP Payload]" + "\n"
        out += payloadString(pkt[UDP])
    return out
