from scapy.all import *

a = IP(dst="141.76.82.170")/UDP(dport=12345)
a.show()
send(a)