from scapy.all import *

a = IP(dst="141.76.82.170")/UDP(sport=33333, dport=12345)/Raw(load=bytes.fromhex("09060001")) # 09 -> keine Ahnung; 06 -> Adresse; 00 -> socket; 01 -> index
# a.show()
send(a)
