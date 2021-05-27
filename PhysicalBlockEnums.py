from Block import Block
from enum import IntEnum


class PhysicalBlockParentClass(IntEnum):
    TRANSMITTER = 1
    ACTUATOR = 2
    DISCRETE_IO = 3
    CONTROLLER = 4
    ANALYSER = 5
    LAB_DEVICE = 6
    MULTI_VARIABLE = 127


class PhysicalBlock(Block):

    def __init__(self, bytz):
        super(bytz)

        if self.block_object_byte != 1:
            raise ValueError("Block Object must be 0x01 in Physical Block! (got {})".format(self.block_object_byte))
        if self.class_byte != 250: 
            raise ValueError("Class must be 0xfa in Physical Block! (got {})".format(self.class_byte))  
    
    def get_parent_class(self) -> PhysicalBlockParentClass:
        return PhysicalBlockParentClass(self.parent_class_byte)