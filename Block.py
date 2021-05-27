from TransducerBlockEnum import TRANSDUCER_BLOCK_CLASSENUM_BY_PARENT, TransducerBlockParentClass
from FunctionBlockEnums import FUNCTION_BLOCK_CLASSENUM_BY_PARENT, FunctionBlockParentClass
from PhysicalBlockEnums import PhysicalBlockParentClass
from utils import bitstring_to_int
from enum import IntEnum


class BlockType(IntEnum):
    PHYSICAL_BLOCK = 1
    FUNCTION_BLOCK = 2
    TRANSDUCER_BLOCK = 3


class Block:

    def __init__(self, bytz, type="bit"):
        # got hex string
        if type == "hex" and isinstance(bytz, str) and len(bytz) == 20*2:
            self.raw_bytes_s = [char for char in bytz]
        # got bitstring
        elif type == "bit" and isinstance(bytz, str) and len(bytz) == 20*8:
            bytz = bitstring_to_int(bytz)
            self.raw_bytes_s = [char for char in hex(bytz)[2:].rjust(40, "0")]
        # got list
        elif type == "list" and isinstance(bytz, list) and len(bytz) == 20:
            self.raw_bytes_s = ""
            for i in range(20): self.raw_bytes_s = self.raw_bytes_s + hex(bytz[i])[2:].rjust(2, "0")
        # got integer
        elif isinstance(bytz, int):
            self.raw_bytes_s = [char for char in hex(bytz)[2:].rjust(40, "0")]
        else:
            raise ValueError()

        self.raw_bytes = []
        for i in range(len(self.raw_bytes_s) / 2):
            self.raw_bytes[i] = int(self.raw_bytes_s[i:i + 1], 16)

        # Block should have 20 bytes

        self.reserved = self.raw_bytes[0] # byte 1, useless
        self.block_object_byte = self.raw_bytes[1] # byte 2
        self.parent_class_byte = self.raw_bytes[2] # byte 3
        self.block_class_byte = self.raw_bytes[3] # byte 4

        self.__parse_block_head()

        self.dd_reference = int(
            self.raw_bytes_s[8:16], 16) # bytes 5-8, useless
        # bytes 9-10, useless
        self.dd_revision = int(self.raw_bytes_s[16:20], 16)

        self.profile = int(self.raw_bytes_s[20:24], 16) # bytes 11-12
        self.profile_revision = int(self.raw_bytes_s[24:28], 16) # bytes 13-14

        self.execution_time = self.raw_bytes[14] # byte 15, useless

        self.no_of_parameters = int(self.raw_bytes_s[30:34], 16) # bytes 16-17

        # bytes 18-19, [slot, index]
        self.addr_of_view_1_slot = self.raw_bytes[17:18]
        self.no_of_views = self.raw_bytes[19] # byte 20

    def __parse_block_head(self):
        self.block_type = BlockType(self.block_object_byte)
        if self.block_type == BlockType.PHYSICAL_BLOCK:
            self.__parse_physical_block_head()
        elif self.block_type == BlockType.FUNCTION_BLOCK:
            self.__parse_function_block_head()
        elif self.block_type == BlockType.TRANSDUCER_BLOCK:
            self.__parse_transducer_block_head()

    def __parse_physical_block_head(self):
        self.parent_class = PhysicalBlockParentClass(self.parent_class_byte)
        self.block_class = None

    def __parse_function_block_head(self):
        self.parent_class = FunctionBlockParentClass(self.parent_class_byte)
        self.block_class = FUNCTION_BLOCK_CLASSENUM_BY_PARENT[self.parent_class](
            self.block_class_byte)

    def __parse_transducer_block_head(self):
        self.parent_class = TransducerBlockParentClass(self.parent_class_byte)
        self.block_class = TRANSDUCER_BLOCK_CLASSENUM_BY_PARENT[self.parent_class](
            self.block_class_byte)
