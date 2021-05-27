from utils import bitstring_to_int

class GenericBlock:

    def __init__(self, bytz):
        # got hex string
        if isinstance(bytz, str) and bytz.find("0x") == 0:
            self.raw_bytes = [int(char) for char in bytz[2:].rjust(4,"0")]
        # got bitstring
        elif isinstance(bytz, str):
            bytz = bitstring_to_int(bytz)
            self.raw_bytes = [int(char) for char in hex(bytz)[2:].rjust(4,"0")]
        # got integer
        elif isinstance(bytz, int):
            self.raw_bytes = [int(char) for char in hex(bytz)[2:].rjust(4,"0")]
        
        self.reserved_byte = self.raw_bytes[0]
        self.block_object_byte = self.raw_bytes[1]
        self.parent_class_byte = self.raw_bytes[2]
        self.class_byte = self.raw_bytes[3]