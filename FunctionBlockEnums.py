from Block import Block
from enum import IntEnum


class FunctionBlockParentClass(IntEnum):
    INPUT = 1
    OUTPUT = 2
    CONTROL = 3
    ADVANCED_CONTROL = 4
    CALCULATION = 5
    AUXILIARY = 6
    ALERT = 7


class FunctionBlockClass(IntEnum):
    pass


class FunctionBlockClassInput(FunctionBlockClass):
    ANALOG_INPUT = 1
    DISCRETE_INPUT = 2


class FunctionBlockClassOutput(FunctionBlockClass):
    ANALOG_OUTPUT = 1
    DISCRETE_OUTPUT = 2


class FunctionBlockClassControl(FunctionBlockClass):
    PID = 1
    SAMPLE_SELECTOR = 2
    LAB_DEVICE_CONTROL = 3


class FunctionBlockClassAdvancedControl(FunctionBlockClass):
    LAB_INSTRUMENTS = 1


class FunctionBlockClassCalculation(FunctionBlockClass):
    TOTALISER = 8


class FunctionBlockClassAuxiliary(FunctionBlockClass):
    RAMP = 1
    BM_LOGBOOK = 2
    SAMPLE = 3


class FunctionBlockClassAlert(FunctionBlockClass):
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
