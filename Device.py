from utils import *
from scapy.all import sr1, IP, UDP, Raw
import random
from Block import Block

class Device_Header:
    def __init__(self, bitstring: str):
        self.dir_id = bitstring_to_int(bitstring[0:16])
        self.rev_number = bitstring_to_int(bitstring[16:32])
        self.num_dir_obj = bitstring_to_int(bitstring[32:48])
        self.num_dir_entry = bitstring_to_int(bitstring[48:64])
        self.first_comp_list_dir_entry = bitstring_to_int(bitstring[64:80])
        self.num_comp_list_dir_entry = bitstring_to_int(bitstring[80:96])

    def __str__(self) -> str:
        return(f"""Header:\nDir ID: {self.dir_id}\nRev Number: {self.rev_number}\nNum_Dir_Obj: {self.num_dir_obj}\nNum_Dir_Entry: {self.num_dir_entry}\nFirst_Comp_List_Dir_Entry: {self.first_comp_list_dir_entry}\nNum_Comp_List_Dir_Entry: {self.num_comp_list_dir_entry}""")
        

class Device:
    def __init__(self, address: int = 0, printLevel: PrintLevel = PrintLevel.ASK) -> None:
        self.address = address
        self.printLevel = printLevel

        # header
        self.header = Device_Header("".zfill(96))
        # composit list directory entrie
        self.begin_pb = 0
        self.no_pb = 0
        self.slot_index_pb = [] # list of dicts : {"slot": 0, "index": 0, "number": 0}
        
        self.begin_tb = 0
        self.no_tb = 0
        self.slot_index_tb = []

        self.begin_fb = 0
        self.no_fb = 0
        self.slot_index_fb = []

        self.begin_lo = 0
        self.no_lo = 0
        self.slot_index_lo = []

    def __str__(self) -> str:
        return(f"""Device at address {self.address}:
        \tNumber PB: {len(self.slot_index_pb)}
        \tNumber TB: {len(self.slot_index_tb)}
        \tNumber FB: {len(self.slot_index_fb)}
        \tNumber LO: {len(self.slot_index_lo)} """)


    def request_header(self):
        # request header
        bitstring = self.__request(0x01, 0x00)
        self.header = Device_Header(bitstring)

        if parse_y_n_input("Show header? [y/n]: ", self.printLevel):
            print(self.header)
            # print(f"""Header:\nDir ID: {bitstring_to_int(bitstring[0:16])}\nRev Number: {bitstring_to_int(bitstring[16:32])}\nNum_Dir_Obj: {bitstring_to_int(self.num_dir_obj)}\nNum_Dir_Entry: {bitstring_to_int(self.num_dir_entry)}\nFirst_Comp_List_Dir_Entry: {bitstring_to_int(self.first_comp_list_dir_entry)}\nNum_Comp_List_Dir_Entry: {bitstring_to_int(self.num_comp_list_dir_entry)}""")

    # make request to remote proxy via scapy stacking and show answer payload
    def request_composit_list_directory(self):
        bitstring = self.__request(0x01, int(self.header.num_dir_obj))
        # print(hex(bitstring_to_int(bitstring)))

        # Physical Block
        self.begin_pb = bitstring[0:16]
        self.no_pb = bitstring[16:32]

        for i in range(0,bitstring_to_int(self.no_pb)):
            self.slot_index_pb.append({"slot": 0, "index": 0, "number": 0})
       
            self.slot_index_pb[i]['slot'] = bitstring_to_int( bitstring[ ((bitstring_to_int(self.begin_pb[8:16])-1) * 32 + ((i)*32)): ((bitstring_to_int(self.begin_pb[8:16])-1) * 32 + 8 + ((i)*32))])
            self.slot_index_pb[i]['index'] = bitstring_to_int( bitstring[ ((bitstring_to_int(self.begin_pb[8:16])-1) * 32 + 8 + ((i)*32)): ((bitstring_to_int(self.begin_pb[8:16])-1) * 32 + 16 + ((i)*32))])
            self.slot_index_pb[i]['number'] = bitstring_to_int( bitstring[ ((bitstring_to_int(self.begin_pb[8:16])-1) * 32 + 16 + ((i)*32)): (((bitstring_to_int(self.begin_pb[8:16])-1) * 32 + 32 + ((i)*32)))])


        # Transducer Block
        self.begin_tb = bitstring[32:48]
        self.no_tb = bitstring[48:64]

        for i in range(0,bitstring_to_int(self.no_tb)):
            self.slot_index_tb.append({"slot": 0, "index": 0, "number": 0})
       
            self.slot_index_tb[i]['slot'] = bitstring_to_int( bitstring[ ((bitstring_to_int(self.begin_tb[8:16])-1) * 32  + ((i)*32)): ((bitstring_to_int(self.begin_tb[8:16])-1) * 32 + 8 + ((i)*32))])
            self.slot_index_tb[i]['index'] = bitstring_to_int( bitstring[ ((bitstring_to_int(self.begin_tb[8:16])-1) * 32 + 8 + ((i)*32)): ((bitstring_to_int(self.begin_tb[8:16])-1) * 32 + 16 + ((i)*32))])
            self.slot_index_tb[i]['number'] = bitstring_to_int( bitstring[ ((bitstring_to_int(self.begin_tb[8:16])-1) * 32 + 16 + ((i)*32)): (((bitstring_to_int(self.begin_tb[8:16])-1) * 32 + 32 + ((i)*32)))])


        # Function Block
        self.begin_fb = bitstring[64:80]
        self.no_fb = bitstring[80:96]

        for i in range(0,bitstring_to_int(self.no_fb)):
            self.slot_index_fb.append({"slot": 0, "index": 0, "number": 0})
       
            self.slot_index_fb[i]['slot'] = bitstring_to_int( bitstring[ ((bitstring_to_int(self.begin_fb[8:16])-1) * 32 + ((i)*32)): ((bitstring_to_int(self.begin_fb[8:16])-1) * 32 + 8 + ((i)*32))])
            self.slot_index_fb[i]['index'] = bitstring_to_int( bitstring[ ((bitstring_to_int(self.begin_fb[8:16])-1) * 32 + 8 + ((i)*32)): ((bitstring_to_int(self.begin_fb[8:16])-1) * 32 + 16 + ((i)*32))])
            self.slot_index_fb[i]['number'] = bitstring_to_int( bitstring[ ((bitstring_to_int(self.begin_fb[8:16])-1) * 32 + 16 + ((i)*32)): (((bitstring_to_int(self.begin_fb[8:16])-1) * 32 + 32 + ((i)*32)))])


        if self.header.num_comp_list_dir_entry >= 4:
            # Link Object
            self.begin_lo = bitstring[96:112]
            self.no_lo = bitstring[112:128]

            for i in range(0,bitstring_to_int(self.no_pb)):
                self.slot_index_lo.append({"slot": 0, "index": 0, "number": 0})
        
                self.slot_index_lo[i]['slot'] = bitstring_to_int( bitstring[ ((bitstring_to_int(self.begin_lo[8:16])-1) * 32 + ((i)*32)): ((bitstring_to_int(self.begin_lo[8:16])-1) * 32 + 8 + ((i)*32))])
                self.slot_index_lo[i]['index'] = bitstring_to_int( bitstring[ ((bitstring_to_int(self.begin_lo[8:16])-1) * 32 + 8 + ((i)*32)): ((bitstring_to_int(self.begin_lo[8:16])-1) * 32 + 16 + ((i)*32))])
                self.slot_index_lo[i]['number'] = bitstring_to_int( bitstring[ ((bitstring_to_int(self.begin_lo[8:16])-1) * 32 + 16 + ((i)*32)): (((bitstring_to_int(self.begin_lo[8:16])-1) * 32 + 32 + ((i)*32)))])


        if parse_y_n_input("Show Composite List Directory Entries? [y/n]: ", self.printLevel):
            print(f"Beging PB:\n\tIndex:\t{bitstring_to_int(self.begin_pb[0:8])}\n\tOffset:\t{hex(bitstring_to_int(self.begin_pb[8:16]))}")
            print(f"\tNumber:\t{bitstring_to_int(self.no_pb)}")
            print(f"Beging TB:\n\tIndex:\t{bitstring_to_int(self.begin_tb[0:8])}\n\tOffset:\t{hex(bitstring_to_int(self.begin_tb[8:16]))}")
            print(f"\tNumber:\t{bitstring_to_int(self.no_tb)}")
            print(f"Beging FB:\n\tIndex:\t{bitstring_to_int(self.begin_fb[0:8])}\n\tOffset:\t{hex(bitstring_to_int(self.begin_fb[8:16]))}")
            print(f"\tNumber:\t{bitstring_to_int(self.no_fb)}")

            if bitstring_to_int(self.header.num_comp_list_dir_entry) >= 4:
                print(f"Beging LO:\n\tIndex:\t{hex(bitstring_to_int(self.begin_pb[0:8]))}\n\tOffset:\t{hex(bitstring_to_int(self.begin_pb[8:16]))}")
                print(f"\tNumber:\t{hex(bitstring_to_int(self.no_pb))}")
        
        if parse_y_n_input("Show start of Blocks? [y/n]: ", self.printLevel):
            for i in range(0,len(self.slot_index_pb)):
                print(f"{i + 1}. PB:\n\tSlot:\t{self.slot_index_pb[i]['slot']}\n\tIndex:\t{self.slot_index_pb[i]['index']}\n\tNumber:\t{self.slot_index_pb[i]['number']}")
            for i in range(0,len(self.slot_index_tb)):
                print(f"{i + 1}. TB:\n\tSlot:\t{self.slot_index_tb[i]['slot']}\n\tIndex:\t{self.slot_index_tb[i]['index']}\n\tNumber:\t{self.slot_index_tb[i]['number']}")
            for i in range(0,len(self.slot_index_fb)):
                print(f"{i + 1}. FB:\n\tSlot:\t{self.slot_index_fb[i]['slot']}\n\tIndex:\t{self.slot_index_fb[i]['index']}\n\tNumber:\t{self.slot_index_fb[i]['number']}")
            for i in range(0,len(self.slot_index_lo)):
                print(f"{i + 1}. LO:\n\tSlot:\t{self.slot_index_lo[i]['slot']}\n\tIndex:\t{self.slot_index_lo[i]['index']}\n\tNumber:\t{self.slot_index_lo[i]['number']}")

    # does the request over UDP and returns bitstring
    def __request(self, slot:int, index:int):
        for x in range(3):
            print(f'Try {x}')
            framemarker = bytes([(0xff & random.randint(0x00, 0xff))])
            a = IP(dst="141.76.82.170")/UDP(sport=33333, dport=12345)/Raw(load=framemarker + bytes([self.address]) + bytes([slot]) + bytes([index]))

            # send and wait for answer
            answer = sr1(a)
            # answer.show()

            # convert "raw" answer to readble hex values
            raw_payload = bytes(answer[Raw])
            # print(framemarker)
            # print(raw_payload.hex())
            raw_payload = raw_payload[1:]
            print(raw_payload)
            if raw_payload != b'':
                return bytes_to_bitstring(raw_payload)
        # TODO Error Handling if three attamps not successful

    def request_block(self, slot:int, index:int):
        payload = self.__request(slot, index)
        # print(hex(bitstring_to_int(payload)))
        return payload
    
    def inspect_block(self, number: int):
        print(f"Inspecting the Block at position {number}")
        block = {"slot": 0, "index": 0}
        if number-1 < bitstring_to_int(self.no_pb):
            block = self.slot_index_pb[number-1]
        elif number-1 < bitstring_to_int(self.no_pb) + bitstring_to_int(self.no_tb):
            block = self.slot_index_tb[number-1 - bitstring_to_int(self.no_pb)]
        elif number-1 < bitstring_to_int(self.no_pb) + bitstring_to_int(self.no_fb) + bitstring_to_int(self.no_tb):
            block = self.slot_index_fb[number-1 - bitstring_to_int(self.no_pb) - bitstring_to_int(self.no_tb)]
        elif number-1 < bitstring_to_int(self.no_pb) + bitstring_to_int(self.no_fb) + bitstring_to_int(self.no_tb) + bitstring_to_int(self.no_lo):
            block = self.slot_index_lo[number-1 - bitstring_to_int(self.no_pb) - bitstring_to_int(self.no_tb) - bitstring_to_int(self.no_fb)]
        
        block_bit_string = self.request_block(block["slot"], block["index"])
        block = Block(block_bit_string, "bit")
        print(block)
