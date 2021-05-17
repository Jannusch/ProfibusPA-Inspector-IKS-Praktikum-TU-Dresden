from scapy.all import *

address = input("Please enter the address:\t")
if int(address) < 10:
    address = "0" + address
address = bytes.fromhex(address)

socket_addr = input("Please enter the socket_addr:\t")
if int(socket_addr) < 10:
    socket_addr = "0" + socket_addr
socket_addr = bytes.fromhex(socket_addr)

index = input("Please enter the index:\t\t")
if int(index) < 10:
    index = "0" + index
index = bytes.fromhex(index)

print(f"09{address}{socket_addr}{index}")
a = IP(dst="141.76.82.170")/UDP(sport=33333, dport=12345)/Raw(load=b'\x09' + address + socket_addr + index) # 09 -> keine Ahnung; 06 -> Adresse; 00 -> socket; 01 -> index
# a.show()
send(a)
