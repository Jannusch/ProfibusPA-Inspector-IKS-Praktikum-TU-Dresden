from PhysicalBlockEnums import PhysicalBlockParentClass
import re

from scapy import sessions
from utils import *
from Device import Device
import argparse
from Block import Block, BlockViewAdapter, ViewBlockAdapter
import sys

# Webserver
from flask import Flask, render_template, request, session
from flask_session import Session

app = Flask(__name__)
app.debug = True
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)
app.add_template_global(bitstring_to_int, name='bitstring_to_int')
app.add_template_global(len, name='len')
app.add_template_global(range, name='range')
app.add_template_global(str, name="str")



@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/inspect_block/")
def inspect_block():
    block_number = request.values.get('number')
    block_type = request.values.get('type')
    device = session.get('device')
    print(block_number, block_type, device)
    block = device.inspect_block(int(block_number), block_type)
    print(block)
    if block.block_class in BlockViewAdapter:
        params = BlockViewAdapter[block.block_class]
    else:
        params = BlockViewAdapter[PhysicalBlockParentClass]
    session['block'] = block
    session['params'] = params
    return render_template("block.html", block=block, device=device, params=params, answer = None)

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

@app.route("/request_optional/", methods = ['POST'])
def request_optional():
    form_data = request.form
    device: Device = session.get('device')

    requested_params = {}
    if form_data['type'] == 'pb/' or form_data['type'] == 'pb':
        block = device.slot_index_pb[int(form_data['number'])]
    if form_data['type'] == 'tb/' or form_data['type'] == 'tb':
        block = device.slot_index_tb[int(form_data['number'])]    
    if form_data['type'] == 'fb/' or form_data['type'] == 'fb':
        block = device.slot_index_fb[int(form_data['number'])]
    if form_data['type'] == 'lo/'or form_data['type'] == 'lo':
        block = device.slot_index_lo[int(form_data['number'])]

    for key  in form_data.keys():
        if key != 'type' and key != 'number':
            block_class, param = key.split('.')

            block_class = ViewBlockAdapter[block_class]
            requested_params[param] = block_class[param]
           
    answer = device.request_additional_information(block, requested_params)
    params = session.get('params')
    block = session.get('block')
    return render_template("block.html", block=block, device=device, params=params, answer=answer, type=form_data['type'][0:2], number=form_data['number'])

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
