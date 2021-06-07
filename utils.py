from enum import Enum, IntEnum

class PrintLevel(Enum):
    FULL = 0
    ASK = 1
    NOTHING = 2

class DataType(IntEnum):
    FLOAT = 0
    VALUESTATUS101 = 1
    VALUESTATUS102 = 2
    DS36 = 3
    DS37 = 4
    DS42 = 5
    DS49 = 6
    DS50 = 7
    DS51 = 8
    DS60 = 9
    DS61 = 10
    DS62 = 11
    DS63 = 12
    DS64 = 13
    DS65 = 14
    DS66 = 15
    DS67 = 16
    DS68 = 17
    OCTETSTRING = 18
    UNSIGNED8 = 19
    UNSIGNED16 = 20
    FLOATFLOAT = 21


def bytes_to_bitstring(b) -> str:
    bitstring = str(bin(int.from_bytes(b, byteorder='big')))[2:]
    return bitstring.rjust(len(b)*8, "0")

def bitstring_to_int(bs: str) -> int:
    return int(bs, 2)

def parse_y_n_input(request: str, printLevel: PrintLevel=PrintLevel.ASK) -> bool:
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