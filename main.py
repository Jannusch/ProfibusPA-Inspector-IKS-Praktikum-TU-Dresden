from utils import *
from Device import Device
import argparse
from Block import Block


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="CLI tool for Profibus PA device inspection")
    parser.add_argument('--address', '-a', metavar="", type=int, help="specifies the address of the device", default=0x06, dest="address")
    parser.add_argument('--print', '-p', choices=["all", "ask", "no"], dest="print", default="ask", help="suppress questions for printing")
    args = parser.parse_args()
    
    if args.print == "all":
        printLvl = PrintLevel.FULL
    elif args.print == "no":
        printLvl = PrintLevel.NOTHING
    else:
        printLvl = PrintLevel.ASK

    device = Device(args.address, printLvl)
    
    device.request_header()
    device.request_composit_list_directory()
    
    number = input("Pleas enter Block Number:")
    device.inspect_block(int(number))

    """block = device.request_block(1, 110)
    print(hex(bitstring_to_int(block)))
    Block(block, "bit")
    """
