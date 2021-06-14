from TransducerBlockEnums import *
from FunctionBlockEnums import *
from PhysicalBlockEnums import PhysicalBlockParentClass
from utils import DataType, DataType, bitstring_to_int
from enum import Enum, IntEnum


class BlockType(IntEnum):
    PHYSICAL_BLOCK = 1
    FUNCTION_BLOCK = 2
    TRANSDUCER_BLOCK = 3


class Block:

    def __init__(self, bytz, type: str = "bit") -> None:
        # got hex string
        if type == "hex" and isinstance(bytz, str) and len(bytz) == 20 * 2:
            self.raw_bytes_s = [char for char in bytz]
        # got bitstring
        elif type == "bit" and isinstance(bytz, str) and len(bytz) == 20 * 8:
            bytz = bitstring_to_int(bytz)
            self.raw_bytes_s = [char for char in hex(bytz)[2:].rjust(40, "0")]
        # got list
        elif type == "list" and isinstance(bytz, list) and len(bytz) == 20:
            self.raw_bytes_s = ""
            for i in range(20):
                self.raw_bytes_s = self.raw_bytes_s + \
                    hex(bytz[i])[2:].rjust(2, "0")
        # got integer
        elif isinstance(bytz, int):
            self.raw_bytes_s = [char for char in hex(bytz)[2:].rjust(40, "0")]
        else:
            raise AttributeError()

        self.raw_bytes_s = ''.join(self.raw_bytes_s)
        self.raw_bytes = []
        for i in range(int(len(self.raw_bytes_s) / 2)):
            self.raw_bytes.append(int(self.raw_bytes_s[2 * i:2 * i + 2], 16))

        print(self.raw_bytes_s)

        # Block should have 20 bytes

        self.reserved = self.raw_bytes[0] # byte 1, useless
        self.block_object_byte = self.raw_bytes[1] # byte 2
        self.parent_class_byte = self.raw_bytes[2] # byte 3
        self.block_class_byte = self.raw_bytes[3] # byte 4

        self.__parse_block_head()

        self.dd_reference = int(
            self.raw_bytes_s[8:16], 16) # bytes 5-8, useless
        # bytes 9-10, useless
        self.dd_revision = int(self.raw_bytes_s[16:20], 16)

        self.profile = int(self.raw_bytes_s[20:24], 16) # bytes 11-12
        self.profile_revision = int(self.raw_bytes_s[24:28], 16) # bytes 13-14

        self.execution_time = self.raw_bytes[14] # byte 15, useless

        self.no_of_parameters = int(self.raw_bytes_s[30:34], 16) # bytes 16-17

        # bytes 18-19, [slot, index]
        self.addr_of_view_1_slot = self.raw_bytes[17:18]
        self.no_of_views = self.raw_bytes[19] # byte 20

    def __str__(self) -> str:
        print(self.__print_block_params())
        return(f"""Blocktype: \t\t{self.block_type.name}\nNumber of params: \t{self.no_of_parameters}""")

    def __parse_block_head(self) -> None:
        self.block_type = BlockType(self.block_object_byte)
        if self.block_type == BlockType.PHYSICAL_BLOCK:
            self.__parse_physical_block_head()
        elif self.block_type == BlockType.FUNCTION_BLOCK:
            self.__parse_function_block_head()
        elif self.block_type == BlockType.TRANSDUCER_BLOCK:
            self.__parse_transducer_block_head()

    def __parse_physical_block_head(self) -> None:
        self.parent_class = PhysicalBlockParentClass(self.parent_class_byte)
        self.block_class = None

    def __parse_function_block_head(self) -> None:
        self.parent_class = FunctionBlockParentClass(self.parent_class_byte)
        if self.block_class_byte > 128:
            self.block_class = FunctionBlockClass.MANUFACTURER_SPECIFIC
        else:
            try:
                self.block_class = FUNCTION_BLOCK_CLASSENUM_BY_PARENT[self.parent_class](
                    self.block_class_byte)
            except ValueError:
                self.block_class = FunctionBlockClass.RESERVED

    def __parse_transducer_block_head(self) -> None:
        self.parent_class = TransducerBlockParentClass(self.parent_class_byte)
        if self.block_class_byte > 128:
            self.block_class = TransducerBlockClass.MANUFACTURER_SPECIFIC
        else:
            try:
                self.block_class = TRANSDUCER_BLOCK_CLASSENUM_BY_PARENT[self.parent_class](
                    self.block_class_byte)
            except ValueError:
                self.block_class = TransducerBlockClass.RESERVED

    def __print_block_params(self) -> None:
        params = self.parent_class.PARAMS
        print(params.value.keys())


class BlockViewStandardParams(Enum):
    BLOCK_OBJECT = {"type": DataType.DS32, "offset": 0}
    ST_REV = {"type": DataType.UNSIGNED16, "offset": 1}
    TAG_DESC = {"type": DataType.OCTETSTRING, "offset": 2}
    STRATEGY = {"type": DataType.UNSIGNED16, "offset": 3}
    ALERT_KEY = {"type": DataType.UNSIGNED8, "offset": 4}
    TARGET_MODE = {"type": DataType.UNSIGNED8, "offset": 5}
    MODE_BLK = {"type": DataType.DS37, "offset": 6}
    ALARM_SUM = {"type": DataType.DS42, "offset": 7}


class BlockViewAnalogInputParams(Enum):
    OUT = {"type": DataType.VALUESTATUS101, "offset": 10}
    PV_SCALE = {"type": DataType.FLOATFLOAT, "offset": 11}
    OUT_SCALE = {"type": DataType.DS36, "offset": 12}
    LIN_TYPE = {"type": DataType.UNSIGNED8, "offset": 13}
    CHANNEL = {"type": DataType.UNSIGNED16, "offset": 14}
    PV_FTIME = {"type": DataType.FLOAT, "offset": 16}
    FSAFE_TYPE = {"type": DataType.UNSIGNED8, "offset": 17}
    FSAFE_VALUE = {"type": DataType.FLOAT, "offset": 18}
    ALARM_HYS = {"type": DataType.FLOAT, "offset": 19}
    HI_HI_LIM = {"type": DataType.FLOAT, "offset": 21}
    HI_LIM = {"type": DataType.FLOAT, "offset": 23}
    LO_LIM = {"type": DataType.FLOAT, "offset": 25}
    LO_LO_LIM = {"type": DataType.FLOAT, "offset": 27}
    HI_HI_ALM = {"type": DataType.DS39, "offset": 30}
    HI_ALM = {"type": DataType.DS39, "offset": 31}
    LO_ALM = {"type": DataType.DS39, "offset": 32}
    LO_LO_ALM = {"type": DataType.DS39, "offset": 33}
    SIMULATE = {"type": DataType.DS39, "offset": 34}
    OUT_UNIT_TEXT = {"type": DataType.OCTETSTRING, "offset": 35}


class BlockViewTotalizerParams(Enum):
    TOTAL = {"type": DataType.VALUESTATUS101, "offset": 10}
    UNIT_TOT = {"type": DataType.UNSIGNED16, "offset": 11}
    CHANNEL = {"type": DataType.UNSIGNED16, "offset": 12}
    SET_TOT = {"type": DataType.UNSIGNED8, "offset": 13}
    MODE_TOT = {"type": DataType.UNSIGNED8, "offset": 14}
    FAIL_TOT = {"type": DataType.UNSIGNED8, "offset": 15}
    ALARM_HYS = {"type": DataType.FLOAT, "offset": 17}
    HI_HI_LIM = {"type": DataType.FLOAT, "offset": 18}
    HI_LIM = {"type": DataType.FLOAT, "offset": 19}
    LO_LIM = {"type": DataType.FLOAT, "offset": 20}
    LO_LO_LIM = {"type": DataType.FLOAT, "offset": 21}
    HI_HI_ALM = {"type": DataType.DS39, "offset": 22}
    HI_ALM = {"type": DataType.DS39, "offset": 23}
    LO_ALM = {"type": DataType.DS39, "offset": 24}
    LO_LO_ALM = {"type": DataType.DS39, "offset": 25}


class BlockViewTemperatureTCParams(Enum):
    PRIMARY_VALUE = {"type": DataType.VALUESTATUS101, "offset": 8}
    PRIMARY_VALUE_UNIT = {"type": DataType.UNSIGNED16, "offset": 9}
    SECONDARY_VALUE_1 = {"type": DataType.VALUESTATUS101, "offset": 10}
    SECONDARY_VALUE_2 = {"type": DataType.VALUESTATUS101, "offset": 11}
    SENSOR_MEAS_TYPE = {"type": DataType.UNSIGNED8, "offset": 12}
    INPUT_RANGE = {"type": DataType.UNSIGNED8, "offset": 13}
    LIN_TYPE = {"type": DataType.UNSIGNED8, "offset": 14}
    BIAS_1 = {"type": DataType.FLOAT, "offset": 19}
    BIAS_2 = {"type": DataType.FLOAT, "offset": 20}
    UPPER_SENSOR_LIMIT = {"type": DataType.FLOAT, "offset": 21}
    LOWER_SENSOR_LIMIT = {"type": DataType.FLOAT, "offset": 22}
    INPUT_FAULT_GEN = {"type": DataType.UNSIGNED8, "offset": 24}
    INPUT_FAULT_1 = {"type": DataType.UNSIGNED8, "offset": 25}
    INPUT_FAULT_2 = {"type": DataType.UNSIGNED8, "offset": 26}
    SENSOR_WIRE_CHECK_1 = {"type": DataType.UNSIGNED8, "offset": 27}
    SENSOR_WIRE_CHECK_2 = {"type": DataType.UNSIGNED8, "offset": 28}
    MAX_SENSOR_VALUE_1 = {"type": DataType.FLOAT, "offset": 29}
    MIN_SENSOR_VALUE_1 = {"type": DataType.FLOAT, "offset": 30}
    MAX_SENSOR_VALUE_2 = {"type": DataType.FLOAT, "offset": 31}
    MIN_SENSOR_VALUE_2 = {"type": DataType.FLOAT, "offset": 32}
    RJ_TEMP = {"type": DataType.FLOAT, "offset": 33}
    RJ_TYPE = {"type": DataType.UNSIGNED8, "offset": 34}
    EXTERNAL_RJ_VALUE = {"type": DataType.FLOAT, "offset": 35}
    TAB_ENTRY = {"type": DataType.UNSIGNED8, "offset": 45}
    TAB_X_Y_VALUE = {"type": DataType.FLOATFLOAT, "offset": 46}
    TAB_MIN_NUMBER = {"type": DataType.UNSIGNED8, "offset": 47}
    TAB_MAX_NUMBER = {"type": DataType.UNSIGNED8, "offset": 48}
    TAB_OP_CODE = {"type": DataType.UNSIGNED8, "offset": 49}
    TAB_STATUS = {"type": DataType.UNSIGNED8, "offset": 50}
    TAB_ACTUAL_NUMBER = {"type": DataType.UNSIGNED8, "offset": 51}


class BlockViewTemperatureTRParams(Enum):
    PRIMARY_VALUE = {"type": DataType.VALUESTATUS101, "offset": 8}
    PRIMARY_VALUE_UNIT = {"type": DataType.UNSIGNED16, "offset": 9}
    SECONDARY_VALUE_1 = {"type": DataType.VALUESTATUS101, "offset": 10}
    SECONDARY_VALUE_2 = {"type": DataType.VALUESTATUS101, "offset": 11}
    SENSOR_MEAS_TYPE = {"type": DataType.UNSIGNED8, "offset": 12}
    INPUT_RANGE = {"type": DataType.UNSIGNED8, "offset": 13}
    LIN_TYPE = {"type": DataType.UNSIGNED8, "offset": 14}
    BIAS_1 = {"type": DataType.FLOAT, "offset": 19}
    BIAS_2 = {"type": DataType.FLOAT, "offset": 20}
    UPPER_SENSOR_LIMIT = {"type": DataType.FLOAT, "offset": 21}
    LOWER_SENSOR_LIMIT = {"type": DataType.FLOAT, "offset": 22}
    INPUT_FAULT_GEN = {"type": DataType.UNSIGNED8, "offset": 24}
    INPUT_FAULT_1 = {"type": DataType.UNSIGNED8, "offset": 25}
    INPUT_FAULT_2 = {"type": DataType.UNSIGNED8, "offset": 26}
    SENSOR_WIRE_CHECK_1 = {"type": DataType.UNSIGNED8, "offset": 27}
    SENSOR_WIRE_CHECK_2 = {"type": DataType.UNSIGNED8, "offset": 28}
    MAX_SENSOR_VALUE_1 = {"type": DataType.FLOAT, "offset": 29}
    MIN_SENSOR_VALUE_1 = {"type": DataType.FLOAT, "offset": 30}
    MAX_SENSOR_VALUE_2 = {"type": DataType.FLOAT, "offset": 31}
    MIN_SENSOR_VALUE_2 = {"type": DataType.FLOAT, "offset": 32}
    SENSOR_CONNECTION = {"type": DataType.UNSIGNED8, "offset": 36}
    COMP_WIRE1 = {"type": DataType.FLOAT, "offset": 37}
    COMP_WIRE2 = {"type": DataType.FLOAT, "offset": 38}
    TAB_ENTRY = {"type": DataType.UNSIGNED8, "offset": 45}
    TAB_X_Y_VALUE = {"type": DataType.FLOATFLOAT, "offset": 46}
    TAB_MIN_NUMBER = {"type": DataType.UNSIGNED8, "offset": 47}
    TAB_MAX_NUMBER = {"type": DataType.UNSIGNED8, "offset": 48}
    TAB_OP_CODE = {"type": DataType.UNSIGNED8, "offset": 49}
    TAB_STATUS = {"type": DataType.UNSIGNED8, "offset": 50}
    TAB_ACTUAL_NUMBER = {"type": DataType.UNSIGNED8, "offset": 51}


class BlockViewTemperaturePyroParams(Enum):
    PRIMARY_VALUE = {"type": DataType.VALUESTATUS101, "offset": 8}
    PRIMARY_VALUE_UNIT = {"type": DataType.UNSIGNED16, "offset": 9}
    SECONDARY_VALUE_1 = {"type": DataType.VALUESTATUS101, "offset": 10}
    SECONDARY_VALUE_2 = {"type": DataType.VALUESTATUS101, "offset": 11}
    SENSOR_MEAS_TYPE = {"type": DataType.UNSIGNED8, "offset": 12}
    INPUT_RANGE = {"type": DataType.UNSIGNED8, "offset": 13}
    LIN_TYPE = {"type": DataType.UNSIGNED8, "offset": 14}
    BIAS_1 = {"type": DataType.FLOAT, "offset": 19}
    BIAS_2 = {"type": DataType.FLOAT, "offset": 20}
    UPPER_SENSOR_LIMIT = {"type": DataType.FLOAT, "offset": 21}
    LOWER_SENSOR_LIMIT = {"type": DataType.FLOAT, "offset": 22}
    INPUT_FAULT_GEN = {"type": DataType.UNSIGNED8, "offset": 24}
    INPUT_FAULT_1 = {"type": DataType.UNSIGNED8, "offset": 25}
    INPUT_FAULT_2 = {"type": DataType.UNSIGNED8, "offset": 26}
    SENSOR_WIRE_CHECK_1 = {"type": DataType.UNSIGNED8, "offset": 27}
    SENSOR_WIRE_CHECK_2 = {"type": DataType.UNSIGNED8, "offset": 28}
    MAX_SENSOR_VALUE_1 = {"type": DataType.FLOAT, "offset": 29}
    MIN_SENSOR_VALUE_1 = {"type": DataType.FLOAT, "offset": 30}
    MAX_SENSOR_VALUE_2 = {"type": DataType.FLOAT, "offset": 31}
    MIN_SENSOR_VALUE_2 = {"type": DataType.FLOAT, "offset": 32}
    EMISSIVITY = {"type": DataType.FLOAT, "offset": 39}
    PEAK_TRACK = {"type": DataType.UNSIGNED8, "offset": 40}
    DECAY_RATE = {"type": DataType.FLOAT, "offset": 41}
    PEAK_TIME = {"type": DataType.FLOAT, "offset": 42}
    TRACK_HOLD = {"type": DataType.UNSIGNED8, "offset": 43}
    SPECT_FILT_SET = {"type": DataType.UNSIGNED8, "offset": 44}
    TAB_ENTRY = {"type": DataType.UNSIGNED8, "offset": 45}
    TAB_X_Y_VALUE = {"type": DataType.FLOATFLOAT, "offset": 46}
    TAB_MIN_NUMBER = {"type": DataType.UNSIGNED8, "offset": 47}
    TAB_MAX_NUMBER = {"type": DataType.UNSIGNED8, "offset": 48}
    TAB_OP_CODE = {"type": DataType.UNSIGNED8, "offset": 49}
    TAB_STATUS = {"type": DataType.UNSIGNED8, "offset": 50}
    TAB_ACTUAL_NUMBER = {"type": DataType.UNSIGNED8, "offset": 51}

class BlockViewTemperatureTC_RParams(Enum):
    PRIMARY_VALUE = {"type": DataType.VALUESTATUS101, "offset": 8}
    PRIMARY_VALUE_UNIT = {"type": DataType.UNSIGNED16, "offset": 9}
    SECONDARY_VALUE_1 = {"type": DataType.VALUESTATUS101, "offset": 10}
    SECONDARY_VALUE_2 = {"type": DataType.VALUESTATUS101, "offset": 11}
    SENSOR_MEAS_TYPE = {"type": DataType.UNSIGNED8, "offset": 12}
    INPUT_RANGE = {"type": DataType.UNSIGNED8, "offset": 13}
    LIN_TYPE = {"type": DataType.UNSIGNED8, "offset": 14}
    BIAS_1 = {"type": DataType.FLOAT, "offset": 19}
    BIAS_2 = {"type": DataType.FLOAT, "offset": 20}
    UPPER_SENSOR_LIMIT = {"type": DataType.FLOAT, "offset": 21}
    LOWER_SENSOR_LIMIT = {"type": DataType.FLOAT, "offset": 22}
    INPUT_FAULT_GEN = {"type": DataType.UNSIGNED8, "offset": 24}
    INPUT_FAULT_1 = {"type": DataType.UNSIGNED8, "offset": 25}
    INPUT_FAULT_2 = {"type": DataType.UNSIGNED8, "offset": 26}
    SENSOR_WIRE_CHECK_1 = {"type": DataType.UNSIGNED8, "offset": 27}
    SENSOR_WIRE_CHECK_2 = {"type": DataType.UNSIGNED8, "offset": 28}
    MAX_SENSOR_VALUE_1 = {"type": DataType.FLOAT, "offset": 29}
    MIN_SENSOR_VALUE_1 = {"type": DataType.FLOAT, "offset": 30}
    MAX_SENSOR_VALUE_2 = {"type": DataType.FLOAT, "offset": 31}
    MIN_SENSOR_VALUE_2 = {"type": DataType.FLOAT, "offset": 32}
    RJ_TEMP = {"type": DataType.FLOAT, "offset": 33}
    RJ_TYPE = {"type": DataType.UNSIGNED8, "offset": 34}
    EXTERNAL_RJ_VALUE = {"type": DataType.FLOAT, "offset": 35}
    SENSOR_CONNECTION = {"type": DataType.UNSIGNED8, "offset": 36}
    COMP_WIRE1 = {"type": DataType.FLOAT, "offset": 37}
    COMP_WIRE2 = {"type": DataType.FLOAT, "offset": 38}
    TAB_ENTRY = {"type": DataType.UNSIGNED8, "offset": 45}
    TAB_X_Y_VALUE = {"type": DataType.FLOATFLOAT, "offset": 46}
    TAB_MIN_NUMBER = {"type": DataType.UNSIGNED8, "offset": 47}
    TAB_MAX_NUMBER = {"type": DataType.UNSIGNED8, "offset": 48}
    TAB_OP_CODE = {"type": DataType.UNSIGNED8, "offset": 49}
    TAB_STATUS = {"type": DataType.UNSIGNED8, "offset": 50}
    TAB_ACTUAL_NUMBER = {"type": DataType.UNSIGNED8, "offset": 51}


class BlockViewPressureParams(Enum):
    SENSOR_VALUE = {"type": DataType.FLOAT, "offset": 8}
    SENSOR_HI_LIM = {"type": DataType.FLOAT, "offset": 9}
    SENSOR_LO_LIM = {"type": DataType.FLOAT, "offset": 10}
    CAL_POINT_HI = {"type": DataType.FLOAT, "offset": 11}
    CAL_POINT_LO = {"type": DataType.FLOAT, "offset": 12}
    CAL_MIN_SPAN = {"type": DataType.FLOAT, "offset": 13}
    SENSOR_UNIT = {"type": DataType.UNSIGNED16, "offset": 14}
    TRIMMED_VALUE = {"type": DataType.VALUESTATUS101, "offset": 15}
    SENSOR_TYPE = {"type": DataType.UNSIGNED16, "offset": 16}
    SENSOR_SERIAL_NUMBER = {"type": DataType.UNSIGNED32, "offset": 17}
    PRIMARY_VALUE = {"type": DataType.VALUESTATUS101, "offset": 18}
    PRIMARY_VALUE_UNIT = {"type": DataType.UNSIGNED16, "offset": 19}
    PRIMARY_VALUE_TYPE = {"type": DataType.UNSIGNED16, "offset": 20}
    SENSOR_DIAPHRAGM_MATERIAL = {"type": DataType.UNSIGNED16, "offset": 21}
    SENSOR_FILL_FLUID = {"type": DataType.UNSIGNED16, "offset": 22}
    SENSOR_MAX_STATIC_PRESSURE = {"type": DataType.FLOAT, "offset": 23}
    SENSOR_O_RING_MATERIAL = {"type": DataType.UNSIGNED16, "offset": 24}
    PROCESS_CONNECTION_TYPE = {"type": DataType.UNSIGNED16, "offset": 25}
    PROCESS_CONNECTION_MATERIAL = {"type": DataType.UNSIGNED16, "offset": 26}
    TEMPERATURE = {"type": DataType.VALUESTATUS101, "offset": 27}
    TEMPERATURE_UNIT = {"type": DataType.UNSIGNED16, "offset": 28}
    SECONDARY_VALUE_1 = {"type": DataType.VALUESTATUS101, "offset": 29}
    SECONDARY_VALUE_1_UNIT = {"type": DataType.UNSIGNED16, "offset": 30}
    SECONDARY_VALUE_2 = {"type": DataType.VALUESTATUS101, "offset": 31}
    SECONDARY_VALUE_2_UNIT = {"type": DataType.UNSIGNED16, "offset": 32}
    LIN_TYPE = {"type": DataType.UNSIGNED8, "offset": 33}
    SCALE_IN = {"type": DataType.FLOAT, "offset": 34}
    SCALE_OUT = {"type": DataType.FLOAT, "offset": 35}
    LOW_FLOW_CUT_OFF = {"type": DataType.FLOAT, "offset": 36}
    FLOW_LIN_SQRT_POINT = {"type": DataType.FLOAT, "offset": 37}
    TAB_ACTUAL_NUMBER = {"type": DataType.UNSIGNED8, "offset": 38}
    TAB_ENTRY = {"type": DataType.UNSIGNED8, "offset": 39}
    TAB_MAX_NUMBER = {"type": DataType.UNSIGNED8, "offset": 40}
    TAB_MIN_NUMBER = {"type": DataType.UNSIGNED8, "offset": 41}
    TAB_OP_CODE = {"type": DataType.UNSIGNED8, "offset": 42}
    TAB_STATUS = {"type": DataType.UNSIGNED8, "offset": 43}
    TAB_X_Y_VALUE = {"type": DataType.FLOATFLOAT, "offset": 44}
    MAX_SENSOR_VALUE = {"type": DataType.FLOAT, "offset": 45}
    MIN_SENSOR_VALUE = {"type": DataType.FLOAT, "offset": 46}
    MAX_TEMPERATURE = {"type": DataType.FLOAT, "offset": 47}
    MIN_TEMPERATURE = {"type": DataType.FLOAT, "offset": 48}


class BlockViewLevelParams(Enum):
    PRIMARY_VALUE = {"type": DataType.VALUESTATUS101, "offset": 8}
    PRIMARY_VALUE_UNIT = {"type": DataType.UNSIGNED16, "offset": 9}
    LEVEL = {"type": DataType.FLOAT, "offset": 10}
    LEVEL_UNIT = {"type": DataType.UNSIGNED16, "offset": 11}
    SENSOR_VALUE = {"type": DataType.FLOAT, "offset": 12}
    SENSOR_UNIT = {"type": DataType.UNSIGNED16, "offset": 13}
    SECONDARY_VALUE_1 = {"type": DataType.VALUESTATUS101, "offset": 14}
    SECONDARY_VALUE_1_UNIT = {"type": DataType.UNSIGNED16, "offset": 15}
    SECONDARY_VALUE_2 = {"type": DataType.VALUESTATUS101, "offset": 16}
    SECONDARY_VALUE_2_UNIT = {"type": DataType.UNSIGNED16, "offset": 17}
    SENSOR_OFFSET = {"type": DataType.FLOAT, "offset": 18}
    CAL_TYPE = {"type": DataType.UNSIGNED8, "offset": 19}
    CAL_POINT_LO = {"type": DataType.FLOAT, "offset": 20}
    CAL_POINT_HI = {"type": DataType.FLOAT, "offset": 21}
    LEVEL_LO = {"type": DataType.FLOAT, "offset": 22}
    LEVEL_HI = {"type": DataType.FLOAT, "offset": 23}
    LEVEL_OFFSET = {"type": DataType.FLOAT, "offset": 24}
    LIN_TYPE = {"type": DataType.UNSIGNED8, "offset": 25}
    LIN_DIAMETER = {"type": DataType.FLOAT, "offset": 26}
    LIN_VOLUME = {"type": DataType.FLOAT, "offset": 27}
    SENSOR_HIGH_LIMIT = {"type": DataType.FLOAT, "offset": 28}
    SENSOR_LOW_LIMIT = {"type": DataType.FLOAT, "offset": 29}
    MAX_SENSOR_VALUE = {"type": DataType.FLOAT, "offset": 30}
    MIN_SENSOR_VALUE = {"type": DataType.FLOAT, "offset": 31}
    TEMPERATURE = {"type": DataType.FLOAT, "offset": 32}
    TEMPERATURE_UNIT = {"type": DataType.UNSIGNED16, "offset": 33}
    MAX_TEMPERATURE = {"type": DataType.FLOAT, "offset": 34}
    MIN_TEMPERATURE = {"type": DataType.FLOAT, "offset": 35}
    TAB_ENTRY = {"type": DataType.UNSIGNED8, "offset": 36}
    TAB_X_Y_VALUE = {"type": DataType.FLOATFLOAT, "offset": 37}
    TAB_MIN_NUMBER = {"type": DataType.UNSIGNED8, "offset": 38}
    TAB_MAX_NUMBER = {"type": DataType.UNSIGNED8, "offset": 39}
    TAB_OP_CODE = {"type": DataType.UNSIGNED8, "offset": 40}
    TAB_STATUS = {"type": DataType.UNSIGNED8, "offset": 41}
    TAB_ACTUAL_NUMBER = {"type": DataType.UNSIGNED8, "offset": 42}


class BlockViewFlowParams(Enum):
    CALIBR_FACTOR = {"type": DataType.FLOAT, "offset": 8}
    LOW_FLOW_CUTOFF = {"type": DataType.FLOAT, "offset": 9}
    MEASUREMENT_MODE = {"type": DataType.UNSIGNED8, "offset": 10}
    FLOW_DIRECTION = {"type": DataType.UNSIGNED8, "offset": 11}
    ZERO_POINT = {"type": DataType.FLOAT, "offset": 12}
    ZERO_POINT_ADJUST = {"type": DataType.UNSIGNED8, "offset": 13}
    ZERO_POINT_UNIT = {"type": DataType.UNSIGNED16, "offset": 14}
    NOMINAL_SIZE = {"type": DataType.FLOAT, "offset": 15}
    NOMINAL_SIZE_UNITS = {"type": DataType.UNSIGNED16, "offset": 16}
    VOLUME_FLOW = {"type": DataType.VALUESTATUS101, "offset": 17}
    VOLUME_FLOW_UNITS = {"type": DataType.UNSIGNED16, "offset": 18}
    VOLUME_FLOW_LO_LIMIT = {"type": DataType.FLOAT, "offset": 19}
    VOLUME_FLOW_HI_LIMIT = {"type": DataType.FLOAT, "offset": 20}
    MASS_FLOW = {"type": DataType.VALUESTATUS101, "offset": 21}
    MASS_FLOW_UNITS = {"type": DataType.UNSIGNED16, "offset": 22}
    MASS_FLOW_LO_LIMIT = {"type": DataType.FLOAT, "offset": 23}
    MASS_FLOW_HI_LIMIT = {"type": DataType.FLOAT, "offset": 24}
    DENSITY = {"type": DataType.VALUESTATUS101, "offset": 25}
    DENSITY_UNITS = {"type": DataType.UNSIGNED16, "offset": 26}
    DENSITY_LO_LIMIT = {"type": DataType.FLOAT, "offset": 27}
    DENSITY_HI_LIMIT = {"type": DataType.FLOAT, "offset": 28}
    TEMPERATURE = {"type": DataType.VALUESTATUS101, "offset": 29}
    TEMPERATURE_UNITS = {"type": DataType.UNSIGNED16, "offset": 30}
    TEMPERATURE_LO_LIMIT = {"type": DataType.FLOAT, "offset": 31}
    TEMPERATURE_HI_LIMIT = {"type": DataType.FLOAT, "offset": 32}
    VORTEX_FREQ = {"type": DataType.VALUESTATUS101, "offset": 33}
    VORTEX_FREQ_UNITS = {"type": DataType.UNSIGNED16, "offset": 34}
    VORTEX_FREQ_LO_LIMIT = {"type": DataType.FLOAT, "offset": 35}
    VORTEX_FREQ_HI_LIMIT = {"type": DataType.FLOAT, "offset": 36}
    SOUND_VELOCITY = {"type": DataType.VALUESTATUS101, "offset": 37}
    SOUND_VELOCITY_UNITS = {"type": DataType.UNSIGNED16, "offset": 38}
    SOUND_VELOCITY_LO_LIMIT = {"type": DataType.FLOAT, "offset": 39}
    SOUND_VELOCITY_HI_LIMIT = {"type": DataType.FLOAT, "offset": 40}
    SAMPLING_FREQ = {"type": DataType.VALUESTATUS101, "offset": 41}
    SAMPLING_FREQ_UNITS = {"type": DataType.UNSIGNED16, "offset": 42}


BlockViewAdapter = {
    FunctionBlockClassInput.ANALOG_INPUT: BlockViewAnalogInputParams,

    FunctionBlockClassCalculation.TOTALISER: BlockViewTotalizerParams,

    TransducerBlockClassFlow.ELECTROMAGNETIC: BlockViewFlowParams,
    TransducerBlockClassFlow.VORTEX: BlockViewFlowParams,
    TransducerBlockClassFlow.CORIOLIS: BlockViewFlowParams,
    TransducerBlockClassFlow.THERMAL_MASS: BlockViewFlowParams,
    TransducerBlockClassFlow.ULTRASONIC: BlockViewFlowParams,
    TransducerBlockClassFlow.VARIABLE_AREA: BlockViewFlowParams,
    TransducerBlockClassFlow.DIFFERENTIAL_PRESSURE: BlockViewFlowParams,

    TransducerBlockClassPressure.DIFFERENTIAL: BlockViewPressureParams,
    TransducerBlockClassPressure.ABSOLUTE: BlockViewPressureParams,
    TransducerBlockClassPressure.GAGE: BlockViewPressureParams,
    TransducerBlockClassPressure.PRESSURE_LEVEL_FLOW: BlockViewPressureParams,
    TransducerBlockClassPressure.PRESSURE_LEVEL: BlockViewPressureParams,
    TransducerBlockClassPressure.PRESSURE_FLOW: BlockViewPressureParams,
    TransducerBlockClassPressure.MIXED_PRESSURE: BlockViewPressureParams,

    TransducerBlockClassLevel.HYDROSTATIC: BlockViewLevelParams,
    TransducerBlockClassLevel.ECHO_LEVEL: BlockViewLevelParams,
    TransducerBlockClassLevel.RADIOMETRIC: BlockViewLevelParams,
    TransducerBlockClassLevel.CAPACITY: BlockViewLevelParams,

    TransducerBlockClassTemperature.THERMOCOUPLE: BlockViewTemperatureTCParams,
    TransducerBlockClassTemperature.TC: BlockViewTemperatureTCParams,
    TransducerBlockClassTemperature.RESISTANCE_THERMOMETER: BlockViewTemperatureTRParams,
    TransducerBlockClassTemperature.RTD: BlockViewTemperatureTRParams,
    TransducerBlockClassTemperature.PYROMETER: BlockViewTemperaturePyroParams,
    TransducerBlockClassTemperature.TC_DC: BlockViewTemperatureTCParams,
    TransducerBlockClassTemperature.RTD_R: BlockViewTemperatureTRParams,
    TransducerBlockClassTemperature.TC_RTD_R_DC: BlockViewTemperatureTC_RParams,
}
