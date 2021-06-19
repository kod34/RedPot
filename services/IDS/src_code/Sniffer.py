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

        #get location
        location()

        #log Ports targeted
        Port_scanner(pkt)

        #log intrusion attacks
        SQLintrusion(pkt)

        XSSintrusion(pkt)

        #log DOS attack
        Flood(pkt)

        LOG.flush()
        LOG_CSV.flush()
        LOG_ports_CSV.flush()
        LOG_ports.flush()


    def run(self):
        sniff(prn=self.inPacket, lfilter=lambda pkt: pkt[Ether].src != Ether().src, store=0, stop_filter=self.stopfilter)
