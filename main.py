import re
from utils import *
from Device import Device
import argparse
from Block import Block
import sys

# Webserver
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/init_with_address/", methods = ['POST'])
def data():
    if request.method == 'POST':
        form_data = request.form
        print(form_data["Field_Address"])

        device = Device(int(form_data["Field_Address"]), PrintLevel.NOTHING)
    
        device.request_header()
        device.request_composit_list_directory()

        return render_template("device.html", device=device)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CLI tool for Profibus PA device inspection")
    parser.add_argument('--address', '-a', metavar="", type=int, help="specifies the address of the device", default=0x06, dest="address")
    parser.add_argument('--print', '-p', choices=["all", "ask", "no"], dest="print", default="ask", help="suppress questions for printing")
    parser.add_argument('--nowebserver', '-n', dest="server", default=True, help="disable the webserver", action='store_false')
    args = parser.parse_args()
    
    if args.print == "all":
        printLvl = PrintLevel.FULL
    elif args.print == "no":
        printLvl = PrintLevel.NOTHING
    else:
        printLvl = PrintLevel.ASK

    if args.server:
        app.run()
        sys.exit(0)

    

    device = Device(args.address, printLvl)
    
    device.request_header()
    device.request_composit_list_directory()
    
    number = input("Pleas enter Block Number:")
    device.inspect_block(int(number))

    """block = device.request_block(1, 110)
    print(hex(bitstring_to_int(block)))
    Block(block, "bit")
    """
    sys.exit(0)
