def bytes_to_bitstring(b) -> str:
    bitstring = str(bin(int.from_bytes(b, byteorder='big')))[2:]
    return bitstring.rjust(len(b)*8, "0")

def bitstring_to_int(bs: str) -> int:
    return int(bs, 2)

def parse_y_n_input(request) -> bool:
    answer = input(request)
    answer.lower()
    while(True):
        if answer == "y" or answer == "yes" or answer == "j":
            return True
        if answer == "n" or answer == "no":
            return False
        answer = input("Wrong input")