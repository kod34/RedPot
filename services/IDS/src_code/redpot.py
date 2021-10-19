from scapy.all import *
from sys import argv
import logging
from datetime import datetime
from Sniffer import *

RED = '\033[91m'
BLUE = '\033[34m'
GREEN = '\033[32m'
ENDC = '\033[0m'

def main():

    logging.basicConfig(filename='/redpot/logs/IDS/all_packets.log', filemode = 'a', level=logging.INFO)

    Sniffer().start()

main()

