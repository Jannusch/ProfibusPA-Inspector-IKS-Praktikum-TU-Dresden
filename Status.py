from enum import IntEnum
from utils import bitstring_to_int


class StatusQuality(IntEnum):
    BAD = 0
    UNCERTAIN = 1
    GOOD_NON_CASCADE = 2
    GOOD_CASCADE = 3


class StatusStubstatus(IntEnum):
    pass


class StatusSubstatusBad(StatusStubstatus):
    NON_SPECIFIC = 0
    CONFIGURATION_ERROR = 1
    NOT_CONNECTED = 2
    DEVICE_FAILURE = 3
    SENSOR_FAILURE = 4
    NO_COM_LAST_VALUE = 5
    NO_COM_NO_VALUE = 6
    OUT_OF_SERVICE = 7


class StatusSubstatusUncertain(StatusStubstatus):
    NON_SPECIFIC = 0
    LAST_USEABLE_VALUE = 1
    SUBSTITUTE_VALUE = 2
    INITIAL_VALUE = 3
    SENSOR_CONVERSION_INACURATE = 4
    ENGINEERING_UNIT_VIOLATION = 5
    SUB_NORMAL = 6
    CONFIGURATION_ERROR = 7
    SIMULATED_VALUE = 8
    SENSOR_CALIBRATION = 9


class StatusSubstatusGoodNonCascade(StatusStubstatus):
    OK = 0
    UPDATE_EVENT = 1
    ACTIVE_ADVISORY_ALARM = 2
    ACTIVE_CRITICAL_ALARM = 3
    UNACKNOWLEDGED_UPDATE_EVENT = 4
    UNACKNOWLEDGED_ADVISORY_ALARM = 5
    UNACKNOWLEDGED_CRITICAL_ALARM = 6
    INITIATE_FAIL_SAFE = 8
    MAINTENANCE_REQUIRED = 9


class StatusSubstatusGoodCascade(StatusStubstatus):
    OK = 0
    INITIALISATION_ACKNOWLEDGED = 1
    INITIALISATION_REQUESTED = 2
    NOT_INVITED = 3
    DO_NOT_SELECT = 5
    LOCAL_OVERRIDE = 6
    INITIATE_FAIL_SAFE = 8


class StatusLimit(IntEnum):
    OK = 0
    LOW_LIMITED = 1
    HIGH_LIMITED = 2
    CONSTANT = 3


class Status:

    def __init__(self, bytz, type:str="bit") -> None:
        if type == "hex" and isinstance(bytz, str) and len(bytz) == 2:
            self.bits = bin(int(bytz, 16))[2:]
        elif type == "bin" and isinstance(bytz, str) and len(bytz) == 8:
            self.bits = bytz
        elif isinstance(bytz, int):
            self.bits = bin(bytz)[2:]

        self.quality = StatusQuality(
            bitstring_to_int(self.bits[0:2])) # first two bits

        if self.quality == StatusQuality.BAD:
            self.substatus = StatusSubstatusBad(
                bitstring_to_int(self.bits[2:6]))
        elif self.quality == StatusQuality.UNCERTAIN:
            self.substatus = StatusSubstatusUncertain(
                bitstring_to_int(self.bits[2:6]))
        elif self.quality == StatusQuality.GOOD_NON_CASCADE:
            self.substatus = StatusSubstatusGoodNonCascade(
                bitstring_to_int(self.bits[2:6]))
        elif self.quality == StatusQuality.GOOD_CASCADE:
            self.substatus = StatusSubstatusGoodCascade(
                bitstring_to_int(self.bits[2:6]))

        self.limit = StatusLimit(bitstring_to_int(self.bits[6:]))

        if self.quality == StatusQuality.GOOD_NON_CASCADE \
            and self.substatus == StatusSubstatusGoodNonCascade.OK \
            and (self.limit == StatusLimit.LOW_LIMITED or self.limit == StatusLimit.HIGH_LIMITED):
            raise ValueError("Status invalid")
        
        if self.quality == StatusQuality.GOOD_CASCADE \
            and self.substatus == StatusSubstatusGoodCascade.OK \
            and (self.limit == StatusLimit.LOW_LIMITED or self.limit == StatusLimit.HIGH_LIMITED):
            raise ValueError("Status invalid")

