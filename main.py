from scapy.all import *
import sys
import binascii

def read_params(param_list):
    address = input("Please enter the address:\t")
    if int(address) < 10:
        address = "0" + address
    param_list["address"] = bytes.fromhex(address)

    socket_addr = input("Please enter the socket_addr:\t")
    if int(socket_addr) < 10:
        socket_addr = "0" + socket_addr
    param_list["socket_addr"] = bytes.fromhex(socket_addr)

    index = input("Please enter the index:\t\t")
    if int(index) < 10:
        index = "0" + index
    param_list["index"] = bytes.fromhex(index)

    print(f"{param_list['framemarker']}{address}{socket_addr}{index}")
    return param_list

def request(param_list):
    print(param_list)

    a = IP(dst="141.76.82.170")/UDP(sport=33333, dport=12345)/Raw(load=param_list["framemarker"] + param_list["address"] + param_list["socket_addr"] + param_list["index"]) # 09 -> keine Ahnung; 06 -> Adresse; 00 -> socket; 01 -> index

    awnser = sr1(a)
    awnser.show()

    payload = bytes(awnser[Raw]).hex()
    print(payload)


if __name__ == "__main__":
    
    param_list = {
        "framemarker": bytes([(0xff & random.randint(0x00, 0xff))]),
        "address": bytes([0x06]),
        "socket_addr": bytes([0x01]),
        "index": bytes([0x01])
    }

    if len(sys.argv) > 1:
        param_list = read_params(param_list)

    request(param_list)

