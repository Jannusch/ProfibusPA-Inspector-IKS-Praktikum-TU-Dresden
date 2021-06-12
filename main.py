import re

from scapy import sessions
from utils import *
from Device import Device
import argparse
from Block import Block
import sys

# Webserver
from flask import Flask, render_template, request, session
from flask_session import Session

app = Flask(__name__)
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)
app.add_template_global(bitstring_to_int, name='bitstring_to_int')
app.add_template_global(len, name='len')
app.add_template_global(range, name='range')



@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/inspect_block/")
def inspect_block():
    block_number = request.values.get('number')
    block_type = request.values.get('type')
    device = session.get('device')

    block = device.inspect_block(int(block_number), block_type)
    return render_template("block.html", block=block, device=device)

@app.route("/init_with_address/", methods = ['POST'])
def data():
    if request.method == 'POST':
        form_data = request.form
        print(form_data["Field_Address"])

        device = Device(int(form_data["Field_Address"]), PrintLevel.NOTHING)
    
        device.request_header()
        device.request_composit_list_directory()
        session['device'] = device

        return render_template("device.html", device=device)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tool for Profibus PA device inspection")
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
