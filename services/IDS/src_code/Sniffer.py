from threading import Thread
from scapy.all import *
import logging
from intrusion import *


class Sniffer(Thread):
    """Thread responsible for sniffing and detecting suspect packet."""

    def __init__(self):
        Thread.__init__(self)
        self.stopped = False

    def stop(self):
        self.stopped = True

    def stopfilter(self, x):
        return self.stopped


    def inPacket(self, pkt):
        """Directive for each received packet."""
  
        logMessage = datetime.now().strftime("%d/%m/%Y %H:%M:%S")+"\r\n"+packetString(pkt)
        logging.warning(logMessage)
        #To update geolocation database
        lease()

        #log Traffic
        traffic()

        #log Ports targeted
        Port_scanner()

        #log SQL injection attacks
        SQLintrusion()

        #log XSS attacks
        XSSintrusion()

        #log DOS attack
        Flood()

        #log SSH bruteforce
        SSH_Flood()

        #flush log files
        LOG.flush()
        LOG_CSV.flush()
        LOG_ports_CSV.flush()
        LOG_ports.flush()
        LOG_traffic_CSV.flush()
        LOG_traffic.flush()
        lease_dates.flush()

    def run(self):
        sniff(prn=self.inPacket, lfilter=lambda pkt: pkt[Ether].src != Ether().src, store=0, stop_filter=self.stopfilter)

