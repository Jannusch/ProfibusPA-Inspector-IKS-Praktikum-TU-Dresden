from utils import *
from Device import Device
import argparse


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="CLI tool for Profibus PA device inspection")
    parser.add_argument('--address', '-a', metavar="", type=int, help="specifies the address of the device", default=0x06, dest="address")
    parser.add_argument('--print', '-p', choices=["all", "no"], dest="print", required=False, help="suppress questions for printing")
    args = parser.parse_args()

    device = Device(args.address)
    if args.print == "all":
        device.printLevel = PrintLevel.Full
    if args.print == "no":
        device.printLevel = PrintLevel.Nothing

    
    device.request_header()
    device.request_composit_list_directory()
