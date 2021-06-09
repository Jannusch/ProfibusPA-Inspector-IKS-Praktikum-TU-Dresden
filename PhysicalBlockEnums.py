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
    PARAMS = {
        "SOFTWARE_REVESION" :
            {
                "type": DataType.VISIBLESTRING,
                "offset": 8
            },
        "HARDWARE_REVISION":
            {
                "type": DataType.VISIBLESTRING,
                "offset": 9
            },
        "DEVICE_MAN_ID":
            {
                "type": DataType.UNSIGNED16,
                "offset": 10
            },
        "DEVICE_ID":
            {
                "type": DataType.VISIBLESTRING,
                "offset": 11
            },
        "DEVICE_SER_NUM":
            {
                "type": DataType.VISIBLESTRING,
                "offset": 12
            },
        "DIAGNOSIS" :
            {
                "type": DataType.OCTETSTRING,
                "offset": 13
            },
        "DIAGNOSIS_EXTENSION":
            {
                "type": DataType.OCTETSTRING,
                "offset": 14
            },
        "DIAGNOSIS_MASK":
            {
                "type": DataType.OCTETSTRING,
                "offset": 15
            },
        "DIAGNOSIS_MASK_EXTENSION":
            {
                "type": DataType.OCTETSTRING,
                "offset": 16
            },
        "DEVICE_CERTIFICATION":
            {
                "type": DataType.VISIBLESTRING,
                "offset": 17
            },
        "WRITE_LOCKING":
            {
                "type": DataType.UNSIGNED16,
                "offset": 18
            },
        "FACTORY_RESET" :
            {
                "type": DataType.UNSIGNED16,
                "offset": 19
            },
        "DESCRIPTOR":
            {
                "type": DataType.OCTETSTRING,
                "offset": 20
            },
        "DEVICE_MESSAGE":
            {
                "type": DataType.OCTETSTRING,
                "offset": 21
            },
        "DEVICE_INSTAL_DATE":
            {
                "type": DataType.OCTETSTRING,
                "offset": 22
            },
        "LOCAL_OP_ENA":
            {
                "type": DataType.UNSIGNED8,
                "offset": 23
            },
        "IDENT_NUMBER_SELECTOR":
            {
                "type": DataType.UNSIGNED8,
                "offset": 24
            },
        "HW_WRITE_PROTECTION":
            {
                "type": DataType.UNSIGNED8,
                "offset": 25
            },
        "FEATURE":
            {
                "type": DataType.DS68,
                "offset": 26
            }
    }


