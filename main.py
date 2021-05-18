from scapy.all import *
import sys
import binascii

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

# make request to remote proxy via scapy stacking and show answer payload
def request(param_list):
    print(param_list)

    # build package with scapy stacking method -> IP()/UDP()/Raw()
    a = IP(dst="141.76.82.170")/UDP(sport=33333, dport=12345)/Raw(load=param_list["framemarker"] + param_list["address"] + param_list["slot"] + param_list["index"]) # 09 -> keine Ahnung; 06 -> Adresse; 00 -> socket; 01 -> index

    # send and wait for answer
    answer = sr1(a)
    answer.show()

    # convert "raw" answer to readble hex values
    raw_payload = bytes(answer[Raw])
    print(raw_payload.hex())
    print(str(bin(bits_from_bytes(raw_payload, 0, 8))))

# get specific bits from an byte object
def bits_from_bytes(bytes_object, index, number):
    # with help and optimizations from https://stackoverflow.com/a/20910950
    mask = 2 ** number - 1
    value = int.from_bytes(bytes_object, byteorder='big')
    
    return value >> (len(bytes_object) * 8 - (index + number)) & mask

if __name__ == "__main__":
    
    # default param list for pressure sensor
    param_list = {
        # cretas frammarker with random offset
        "framemarker": bytes([(0xff & random.randint(0x00, 0xff))]),
        # address for the device ABB Pressure sensor: 06; ABB Temp sensor 07
        "address": bytes([0x06]),
        "slot": bytes([0x01]),
        "index": bytes([0x01])
    }

    # if there is an optional cli arg you will be asked for the param_list values
    if len(sys.argv) > 1:
        param_list = read_params(param_list)

    # make request
    request(param_list)

