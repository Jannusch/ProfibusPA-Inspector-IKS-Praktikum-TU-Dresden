from codecs import decode
import struct
from enum import Enum, IntEnum


class PrintLevel(Enum):
    FULL = 0
    ASK = 1
    NOTHING = 2


class DataType(IntEnum):
    FLOAT = 0
    VALUESTATUS101 = 1
    VALUESTATUS102 = 2
    DS32 = 3
    DS36 = 4
    DS37 = 5
    DS39 = 6
    DS42 = 7
    DS49 = 8
    DS50 = 9
    DS51 = 10
    DS60 = 11
    DS61 = 12
    DS62 = 13
    DS63 = 14
    DS64 = 15
    DS65 = 16
    DS66 = 17
    DS67 = 18
    DS68 = 19
    OCTETSTRING = 20
    UNSIGNED8 = 21
    UNSIGNED16 = 22
    UNSIGNED32 = 23
    FLOATFLOAT = 24
    VISIBLESTRING = 25


# https://stackoverflow.com/a/8762541
# https://creativecommons.org/licenses/by-sa/4.0/


def bin_to_float(b):
    """ Convert binary string to a float. """
    bf = int(b, 2).to_bytes(4, "big")  # 8 bytes needed for IEEE 754 binary64.
    return struct.unpack('>f', bf)[0]

# https://stackoverflow.com/a/8762541
# https://creativecommons.org/licenses/by-sa/4.0/


def int_to_bytes(n, length):  # Helper function
    """ Int/long to byte string.

        Python 3.2+ has a built-in int.to_bytes() method that could be used
        instead, but the following works in earlier versions including 2.x.
    """
    return decode('%%0%dx' % (length << 1) % n, 'hex')[-length:]


def bytes_to_bitstring(b) -> str:
    bitstring = str(bin(int.from_bytes(b, byteorder='big')))[2:]
    return bitstring.rjust(len(b) * 8, "0")


def bitstring_to_int(bs: str) -> int:
    return int(bs, 2)


def parse_y_n_input(request: str, printLevel: PrintLevel = PrintLevel.ASK) -> bool:
    if printLevel == PrintLevel.FULL:
        return True
    if printLevel == PrintLevel.NOTHING:
        return False

    if printLevel == PrintLevel.ASK:
        answer = input(request)
        answer.lower()
        while(True):
            if answer == "y" or answer == "yes" or answer == "j":
                return True
            elif answer == "n" or answer == "no":
                return False
            else:
                answer = input("Wrong input")
