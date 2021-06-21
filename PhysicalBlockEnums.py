from enum import Enum
from utils import DataType


class PhysicalBlockParentClass(Enum):
    TRANSMITTER = 1
    ACTUATOR = 2
    DISCRETE_IO = 3
    CONTROLLER = 4
    ANALYSER = 5
    LAB_DEVICE = 6
    MULTI_VARIABLE = 127


class PhysicalBlockClass(Enum):
    PHYSICAL_BLOCK = 1
