from utils import *
from Block import Block
from Status import Status


def parse_response(value: str, type: DataType) -> str:
    if type == DataType.VALUESTATUS101:
        return f"Value: {bin_to_float(value[:32])} | Status:  {Status(value[32:]).quality.name}"
    elif type == DataType.VALUESTATUS102:
        return f"Value: {bitstring_to_int(value[:32])}| Status: {Status(value[32:]).quality.name}"
    elif type == DataType.FLOAT:
        return f"Value: {bin_to_float(value)}"
    elif type == DataType.FLOATFLOAT:
        return f"X-Value: {bin_to_float(value[:32])} | Y-Value: {bin_to_float(value[32:])}"
    elif type == DataType.UNSIGNED8 or type == DataType.UNSIGNED16 or type == DataType.UNSIGNED32:
        return f"Value: {bitstring_to_int(value)}"
    elif type == DataType.OCTETSTRING:
        text = ""
        for i in range(len(value) // 8):
            asc_val = bitstring_to_int(value[8 * i:8 * i + 8])
            text = text + chr(asc_val)
        return f"String: {text}"
    elif type == DataType.DS32:
        return str(Block(value))
    elif type == DataType.DS36:
        eu100 = bin_to_float(value[:32])
        eu0 = bin_to_float(value[32:64])
        u_index = bitstring_to_int(value[64:80])
        dec_p = bitstring_to_int(value[81:])
        if value[80] == "1":
            dec_p = dec_p * -1
        return f"EU at 100%: {eu100} | EU at 0%: {eu0}  | Units Index: {u_index} | Decimal Point: {dec_p}"
    elif type == DataType.DS37:
        actual = bitstring_to_int(value[:8])
        permitted = bitstring_to_int(value[8:16])
        normal = bitstring_to_int(value[16:])
        return f"Actual:  {actual}  | Permitted:  {permitted}  | Normal:  {normal}"
    elif type == DataType.DS39:
        unack = bitstring_to_int(value[:8])
        a_state = bitstring_to_int(value[8:16])
        timestamp = bitstring_to_int(value[16:80])
        subcode = bitstring_to_int(value[80:96])
        val = bin_to_float(value[96:])
        return f"Unacknowledged: {unack} | Alarm State:  {a_state}  | Timestamp:  {timestamp}  | Subcode: {subcode} | Value: {val}"
    elif type == DataType.DS42:
        alarms = []
        if value[0] == "1":
            alarms.append("Discrete Alarm")
        if value[1] == "1":
            alarms.append("HI HI Alarm")
        if value[2] == "1":
            alarms.append("HI Alarm")
        if value[3] == "1":
            alarms.append("LO LO Alarm")
        if value[4] == "1":
            alarms.append("LO Alarm")
        if value[7] == "1":
            alarms.append("Update Event")
        return ",".join(alarms)