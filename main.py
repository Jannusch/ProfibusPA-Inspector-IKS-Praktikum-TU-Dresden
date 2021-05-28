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
        self.slot_index_pb = []
        
        self.begin_tb = 0
        self.no_tb = 0
        self.slot_index_tb = []

        self.begin_fb = 0
        self.no_fb = 0
        self.slot_index_fb = []

        self.begin_lo = 0
        self.no_lo = 0
        self.slot_index_lo = []

    def request_header(self):
        framemarker = bytes([(0xff & random.randint(0x00, 0xff))])
        a = IP(dst="141.76.82.170")/UDP(sport=33333, dport=12345)/Raw(load=framemarker + bytes([self.address]) + bytes([0x01]) + bytes([0x00]))
        answer = sr1(a)

        raw_payload = bytes(answer[Raw])
        bitstring = bytes_to_bitstring(raw_payload)

        self.num_dir_obj = bitstring[40:56]
        self.num_dir_entry = bitstring[56:72]
        self.first_comp_list_dir_entry = bitstring[72:88]
        self.num_comp_list_dir_entry = bitstring[88:104]
        
        if parse_y_n_input("Show header? [y/n]: "):
            print(f"""Header:\nDir ID: {bitstring_to_int(bitstring[8:24])}\nRev Number: {bitstring_to_int(bitstring[24:40])}\nNum_Dir_Obj: {bitstring_to_int(self.num_dir_obj)}\nNum_Dir_Entry: {bitstring_to_int(self.num_dir_entry)}\nFirst_Comp_List_Dir_Entry: {bitstring_to_int(self.first_comp_list_dir_entry)}\nNum_Comp_List_Dir_Entry: {bitstring_to_int(self.num_comp_list_dir_entry)}""")

    # make request to remote proxy via scapy stacking and show answer payload
    def request_composit_list_directory(self):
        # build package with scapy stacking method -> IP()/UDP()/Raw()
        framemarker = bytes([(0xff & random.randint(0x00, 0xff))])
        a = IP(dst="141.76.82.170")/UDP(sport=33333, dport=12345)/Raw(load=framemarker + bytes([self.address]) + bytes([0x01]) + bytes([int(self.num_dir_obj)]))

        # send and wait for answer
        answer = sr1(a)
        # answer.show()

        # convert "raw" answer to readble hex values
        raw_payload = bytes(answer[Raw])
        # print(raw_payload.hex())

        bitstring = bytes_to_bitstring(raw_payload)

        # Physical Block
        self.begin_pb = bitstring[8:24]
        self.no_pb = bitstring[24:40]

        for i in range(0,bitstring_to_int(self.no_pb)):
            self.slot_index_pb.append({"slot": 0, "index": 0, "number": 0})
       
            self.slot_index_pb[i]['slot'] = bitstring_to_int( bitstring[ ((bitstring_to_int(self.begin_pb[8:16])-1) * 32 + 8 + ((i)*32)): ((bitstring_to_int(self.begin_pb[8:16])-1) * 32 + 16 + ((i)*32))])
            self.slot_index_pb[i]['index'] = bitstring_to_int( bitstring[ ((bitstring_to_int(self.begin_pb[8:16])-1) * 32 + 16 + ((i)*32)): ((bitstring_to_int(self.begin_pb[8:16])-1) * 32 + 24 + ((i)*32))])
            self.slot_index_pb[i]['number'] = bitstring_to_int( bitstring[ ((bitstring_to_int(self.begin_pb[8:16])-1) * 32 + 24 + ((i)*32)): (((bitstring_to_int(self.begin_pb[8:16])-1) * 32 + 40 + ((i)*32)))])


        # Transducer Block
        self.begin_tb = bitstring[40:56]
        self.no_tb = bitstring[56:72]

        for i in range(0,bitstring_to_int(self.no_tb)):
            self.slot_index_tb.append({"slot": 0, "index": 0, "number": 0})
       
            self.slot_index_tb[i]['slot'] = bitstring_to_int( bitstring[ ((bitstring_to_int(self.begin_tb[8:16])-1) * 32 + 8 + ((i)*32)): ((bitstring_to_int(self.begin_tb[8:16])-1) * 32 + 16 + ((i)*32))])
            self.slot_index_tb[i]['index'] = bitstring_to_int( bitstring[ ((bitstring_to_int(self.begin_tb[8:16])-1) * 32 + 16 + ((i)*32)): ((bitstring_to_int(self.begin_tb[8:16])-1) * 32 + 24 + ((i)*32))])
            self.slot_index_tb[i]['number'] = bitstring_to_int( bitstring[ ((bitstring_to_int(self.begin_tb[8:16])-1) * 32 + 24 + ((i)*32)): (((bitstring_to_int(self.begin_tb[8:16])-1) * 32 + 40 + ((i)*32)))])


        # Function Block
        self.begin_fb = bitstring[72:88]
        self.no_fb = bitstring[88:104]

        for i in range(0,bitstring_to_int(self.no_pb)):
            self.slot_index_fb.append({"slot": 0, "index": 0, "number": 0})
       
            self.slot_index_fb[i]['slot'] = bitstring_to_int( bitstring[ ((bitstring_to_int(self.begin_fb[8:16])-1) * 32 + 8 + ((i)*32)): ((bitstring_to_int(self.begin_fb[8:16])-1) * 32 + 16 + ((i)*32))])
            self.slot_index_fb[i]['index'] = bitstring_to_int( bitstring[ ((bitstring_to_int(self.begin_fb[8:16])-1) * 32 + 16 + ((i)*32)): ((bitstring_to_int(self.begin_fb[8:16])-1) * 32 + 24 + ((i)*32))])
            self.slot_index_fb[i]['number'] = bitstring_to_int( bitstring[ ((bitstring_to_int(self.begin_fb[8:16])-1) * 32 + 24 + ((i)*32)): (((bitstring_to_int(self.begin_fb[8:16])-1) * 32 + 40 + ((i)*32)))])


        if bitstring_to_int(self.num_comp_list_dir_entry) >= 4:
            # Link Object
            self.begin_lo = bitstring[104:120]
            self.no_lo = bitstring[120:136]

            for i in range(0,bitstring_to_int(self.no_pb)):
                self.slot_index_lo.append({"slot": 0, "index": 0, "number": 0})
        
                self.slot_index_lo[i]['slot'] = bitstring_to_int( bitstring[ ((bitstring_to_int(self.begin_lo[8:16])-1) * 32 + 8 + ((i)*32)): ((bitstring_to_int(self.begin_lo[8:16])-1) * 32 + 16 + ((i)*32))])
                self.slot_index_lo[i]['index'] = bitstring_to_int( bitstring[ ((bitstring_to_int(self.begin_lo[8:16])-1) * 32 + 16 + ((i)*32)): ((bitstring_to_int(self.begin_lo[8:16])-1) * 32 + 24 + ((i)*32))])
                self.slot_index_lo[i]['number'] = bitstring_to_int( bitstring[ ((bitstring_to_int(self.begin_lo[8:16])-1) * 32 + 24 + ((i)*32)): (((bitstring_to_int(self.begin_lo[8:16])-1) * 32 + 40 + ((i)*32)))])


        if parse_y_n_input("Show Composite List Directory Entries? [y/n]: "):
            print(f"Beging PB:\n\tIndex:\t{hex(bitstring_to_int(self.begin_pb[0:8]))}\n\tOffset:\t{hex(bitstring_to_int(self.begin_pb[8:16]))}")
            print(f"\tNumber:\t{hex(bitstring_to_int(self.no_pb))}")
            print(f"Beging TB:\n\tIndex:\t{hex(bitstring_to_int(self.begin_tb[0:8]))}\n\tOffset:\t{hex(bitstring_to_int(self.begin_tb[8:16]))}")
            print(f"\tNumber:\t{hex(bitstring_to_int(self.no_tb))}")
            print(f"Beging FB:\n\tIndex:\t{hex(bitstring_to_int(self.begin_fb[0:8]))}\n\tOffset:\t{hex(bitstring_to_int(self.begin_fb[8:16]))}")
            print(f"\tNumber:\t{hex(bitstring_to_int(self.no_fb))}")

            if bitstring_to_int(self.num_comp_list_dir_entry) >= 4:
                print(f"Beging LO:\n\tIndex:\t{hex(bitstring_to_int(self.begin_pb[0:8]))}\n\tOffset:\t{hex(bitstring_to_int(self.begin_pb[8:16]))}")
                print(f"\tNumber:\t{hex(bitstring_to_int(self.no_pb))}")
        
        if parse_y_n_input("Show start of Blocks? [y/n]: "):
            for i in range(0,len(self.slot_index_pb)):
                print(f"First PB:\n\tSlot:\t{hex(self.slot_index_pb[i]['slot'])}\n\tIndex:\t{hex(self.slot_index_pb[i]['index'])}\n\tNumber:\t{hex(self.slot_index_pb[i]['number'])}")
            for i in range(0,len(self.slot_index_tb)):
                print(f"First TB:\n\tSlot:\t{hex(self.slot_index_tb[i]['slot'])}\n\tIndex:\t{hex(self.slot_index_tb[i]['index'])}\n\tNumber:\t{hex(self.slot_index_tb[i]['number'])}")
            for i in range(0,len(self.slot_index_fb)):
                print(f"First FB:\n\tSlot:\t{hex(self.slot_index_fb[i]['slot'])}\n\tIndex:\t{hex(self.slot_index_fb[i]['index'])}\n\tNumber:\t{hex(self.slot_index_fb[i]['number'])}")


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
    

def bytes_to_bitstring(b) -> str:
    bitstring = str(bin(int.from_bytes(b, byteorder='big')))[2:]
    return bitstring.rjust(len(b)*8, "0")

def bitstring_to_int(bs: str) -> int:
    return int(bs, 2)

if __name__ == "__main__":

    device = Device()
    device.address = 6 # int(input("Pleas enter the address: ")) 

    # make request
    # request(param_list)
    device.request_header()
    device.request_composit_list_directory()
