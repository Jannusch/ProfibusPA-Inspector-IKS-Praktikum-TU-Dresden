from enum import IntEnum, Enum


class FunctionBlockParentClass(Enum):
    INPUT = 1
    OUTPUT = 2
    CONTROL = 3
    ADVANCED_CONTROL = 4
    CALCULATION = 5
    AUXILIARY = 6
    ALERT = 7
    PARAMS = {
        
    }


class FunctionBlockClass(IntEnum):
    RESERVED = 127
    MANUFACTURER_SPECIFIC = 128


class FunctionBlockClassInput(IntEnum):
    ANALOG_INPUT = 1
    DISCRETE_INPUT = 2


class FunctionBlockClassOutput(IntEnum):
    ANALOG_OUTPUT = 1
    DISCRETE_OUTPUT = 2


class FunctionBlockClassControl(IntEnum):
    PID = 1
    SAMPLE_SELECTOR = 2
    LAB_DEVICE_CONTROL = 3


class FunctionBlockClassAdvancedControl(IntEnum):
    LAB_INSTRUMENTS = 1


class FunctionBlockClassCalculation(IntEnum):
    TOTALISER = 8


class FunctionBlockClassAuxiliary(IntEnum):
    RAMP = 1
    BM_LOGBOOK = 2
    SAMPLE = 3


class FunctionBlockClassAlert(IntEnum):
    pass


FUNCTION_BLOCK_CLASSENUM_BY_PARENT = {
    FunctionBlockParentClass.INPUT: FunctionBlockClassInput,
    FunctionBlockParentClass.OUTPUT: FunctionBlockClassOutput,
    FunctionBlockParentClass.CONTROL: FunctionBlockClassControl,
    FunctionBlockParentClass.ADVANCED_CONTROL: FunctionBlockClassAdvancedControl,
    FunctionBlockParentClass.CALCULATION: FunctionBlockClassCalculation,
    FunctionBlockParentClass.AUXILIARY: FunctionBlockClassAuxiliary,
    FunctionBlockParentClass.ALERT: FunctionBlockClassAlert
}
