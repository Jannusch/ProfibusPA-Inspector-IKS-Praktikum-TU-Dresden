from scapy.all import *
import sys
import binascii
from utils import *
from Device import Device



# ask user for input and try to parse to hex and than byte
# returns the param_list with all params
def read_params(param_list):
    address = input("Please enter the address:\t")
    if int(address) < 10:
        address = "0" + address
    param_list["address"] = bytes.fromhex(address)

    slot = input("Please enter the slot:\t")
    if int(slot) < 10:
        slot = "0" + slot
    param_list["slot"] = bytes.fromhex(slot)

    index = input("Please enter the index:\t\t")
    if int(index) < 10:
        index = "0" + index
    param_list["index"] = bytes.fromhex(index)

    # print(f"{param_list['framemarker']}{address}{slot}{index}")
    return param_list


if __name__ == "__main__":

    device = Device()
    device.address = 6 # int(input("Pleas enter the address: ")) 

    # make request
    # request(param_list)
    device.request_header()
    device.request_composit_list_directory()
