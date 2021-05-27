from scapy.all import *
import sys
import binascii

class Device:
    def __init__(self) -> None:
        self.address = 0
        # header
        self.num_dir_obj = 0
        self.num_dir_entry = 0
        self.first_comp_list_dir_entry = 0
        self.num_comp_list_dir_entry = 0
        # composit list directory entrie
        self.begin_pb = 0
        self.no_pb = 0
        self.begin_tb = 0
        self.no_tb = 0
        self.begin_fb = 0
        self.no_fb = 0
        

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

def parse_y_n_input(request) -> bool:
    answer = input(request)
    answer.lower()
    while(True):
        if answer == "y" or answer == "yes" or answer == "j":
            return True
        if answer == "n" or answer == "no":
            return False
        answer = input("Wrong input")

def request_header(device:Device):
    framemarker = bytes([(0xff & random.randint(0x00, 0xff))])
    a = IP(dst="141.76.82.170")/UDP(sport=33333, dport=12345)/Raw(load=framemarker + bytes([device.address]) + bytes([0x01]) + bytes([0x00])) # 09 -> keine Ahnung; 06 -> Adresse; 00 -> socket; 01 -> index
    answer = sr1(a)

    raw_payload = bytes(answer[Raw])
    bitstring = bytes_to_bitstring(raw_payload)
    device.num_dir_obj = bitstring[40:56]
    device.num_dir_entry = bitstring[56:72]
    device.first_comp_list_dir_entry = bitstring[72:88]
    device.num_comp_list_dir_entry = bitstring[88:104]
    
    if parse_y_n_input("Show header? [y/n]: "):
        print(f"""Header:\nDir ID: {bitstring_to_int(bitstring[8:24])}\nRev Number: {bitstring_to_int(bitstring[24:40])}\nNum_Dir_Obj: {bitstring_to_int(device.num_dir_obj)}\nNum_Dir_Entry: {bitstring_to_int(device.num_dir_entry)}\nFirst_Comp_List_Dir_Entry: {bitstring_to_int(device.first_comp_list_dir_entry)}\nNum_Comp_List_Dir_Entry: {bitstring_to_int(device.num_comp_list_dir_entry)}""")
        # print(f"""Header:\nDir ID: {bitstring[0:16]}\nRev Number: {bitstring_to_int(bitstring[16:32])}\nNum_Dir_Obj: {bitstring_to_int(device.num_dir_obj)}\nNum_Dir_Entry: {bitstring_to_int(device.num_dir_entry)}\nFirst_Comp_List_Dir_Entry: {bitstring_to_int(device.first_comp_list_dir_entry)}\nNum_Comp_List_Dir_Entry: {device.num_comp_list_dir_entry}""")

    

# make request to remote proxy via scapy stacking and show answer payload
def request(param_list):
    # print(param_list)

    # build package with scapy stacking method -> IP()/UDP()/Raw()
    a = IP(dst="141.76.82.170")/UDP(sport=33333, dport=12345)/Raw(load=param_list["framemarker"] + param_list["address"] + param_list["slot"] + param_list["index"]) # 09 -> keine Ahnung; 06 -> Adresse; 00 -> socket; 01 -> index

    # send and wait for answer
    answer = sr1(a)
    # answer.show()

    # convert "raw" answer to readble hex values
    raw_payload = bytes(answer[Raw])
    print(raw_payload.hex())

    bitstring = bytes_to_bitstring(raw_payload)
    print("Framemarker")
    print(bitstring[0:8]) # Framemarker
    print(hex(bitstring_to_int(bitstring[0:8]))) # Framemarker but in hex
    print("\nBegin PB")
    print(bitstring[8:24])
    print(hex(bitstring_to_int(bitstring[8:24])))
    print("unit16: " + str(int('0104', 16)))
    print("No PB")
    print(bitstring[24:40])
    print(bitstring_to_int(bitstring[24:40]))

    
    print("\nBegin TB")
    print(bitstring[40:56])
    print(hex(bitstring_to_int(bitstring[40:56])))
    print("unint16: " + str(int('0105', 16)))
    print("No TB")
    print(bitstring[56:72])
    print(hex(bitstring_to_int(bitstring[56:72])))


    print("\nBegin FB")
    print(bitstring[72:88])
    print(hex(bitstring_to_int(bitstring[72:88])))
    print("unit16: " + str(int('0107', 16)))
    print("No FB")
    print(bitstring[88:104])
    print(hex(bitstring_to_int(bitstring[88:104])))


# get specific bits from an byte object
"""def bits_from_bytes(bytes_object, index, number):
    # with help and optimizations from https://stackoverflow.com/a/20910950
    mask = 2 ** number - 1
    value = int.from_bytes(bytes_object, byteorder='big')
    
    return value >> (len(bytes_object) * 8 - (index + number)) & mask"""

def bytes_to_bitstring(b) -> str:
    bitstring = str(bin(int.from_bytes(b, byteorder='big')))[2:]
    return bitstring.rjust(len(b)*8, "0")

def bitstring_to_int(bs: str) -> int:
    return int(bs, 2)

if __name__ == "__main__":

    device = Device()
    device.address = 6

    
    # default param list for pressure sensor
    param_list = {
        # cretas frammarker with random offset
        "framemarker": bytes([(0xff & random.randint(0x00, 0xff))]),
        # address for the device ABB Pressure sensor: 06; ABB Temp sensor 07
        "address": bytes([0x06]),
        "slot": bytes([0x01]),
        "index": bytes([0x00])
    }

    # if there is an optional cli arg you will be asked for the param_list values
    if len(sys.argv) > 1:
        param_list = read_params(param_list)

    # make request
    # request(param_list)
    request_header(device)
