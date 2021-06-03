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
