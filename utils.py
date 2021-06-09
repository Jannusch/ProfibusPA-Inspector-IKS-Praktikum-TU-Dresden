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
    DS42 = 6
    DS49 = 7
    DS50 = 8
    DS51 = 9
    DS60 = 10
    DS61 = 11
    DS62 = 12
    DS63 = 13
    DS64 = 14
    DS65 = 15
    DS66 = 16
    DS67 = 17
    DS68 = 18
    OCTETSTRING = 19
    UNSIGNED8 = 20
    UNSIGNED16 = 21
    FLOATFLOAT = 22
    VisibleString = 23


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