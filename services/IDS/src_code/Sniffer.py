from threading import Thread
from scapy.all import *
import logging
import json
from PacketStrings import *
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

        #log SQL injection attacks
        SQLintrusion(pkt)

        #log XSS attacks
        XSSintrusion(pkt)



    def run(self):
        sniff(prn=self.inPacket, lfilter=lambda pkt: pkt[Ether].src != Ether().src, store=0, stop_filter=self.stopfilter)
