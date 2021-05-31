from enum import Enum

class PrintLevel(Enum):
    FULL = 0
    ASK = 1
    NOTHING = 2

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