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
    RESERVED = 8

    @classmethod
    def _missing_(cls, value):
        if 8 <= value <= 127:
            return FunctionBlockParentClass.RESERVED
        else:
            raise ValueError()


class FunctionBlockClass(IntEnum):
    pass


class FunctionBlockClassInput(FunctionBlockClass):
    ANALOG_INPUT = 1
    DISCRETE_INPUT = 2
    RESERVED = 3

    @classmethod
    def _missing_(cls, value):
        if 3 <= value <= 127:
            return FunctionBlockClassInput.RESERVED
        else:
            raise ValueError()


class FunctionBlockClassOutput(FunctionBlockClass):
    ANALOG_OUTPUT = 1
    DISCRETE_OUTPUT = 2
    RESERVED = 3

    @classmethod
    def _missing_(cls, value):
        if 3 <= value <= 127:
            return FunctionBlockClassOutput.RESERVED
        else:
            raise ValueError()


class FunctionBlockClassControl(FunctionBlockClass):
    PID = 1
    SAMPLE_SELECTOR = 2
    LAB_DEVICE_CONTROL = 3
    RESERVED = 4

    @classmethod
    def _missing_(cls, value):
        if 4 <= value <= 127:
            return FunctionBlockClassControl.RESERVED
        else:
            raise ValueError()


class FunctionBlockClassAdvancedControl(FunctionBlockClass):
    LAB_INSTRUMENTS = 1
    RESERVED = 2

    @classmethod
    def _missing_(cls, value):
        if 2 <= value <= 127:
            return FunctionBlockClassAdvancedControl.RESERVED
        else:
            raise ValueError()


class FunctionBlockClassCalculation(FunctionBlockClass):
    RESERVED = 1
    TOTALISER = 8

    @classmethod
    def _missing_(cls, value):
        if 1 <= value <= 7 or 9 <= value <= 127:
            return FunctionBlockClassCalculation.RESERVED
        else:
            raise ValueError()


class FunctionBlockClassAuxiliary(FunctionBlockClass):
    RAMP = 1
    BM_LOGBOOK = 2
    SAMPLE = 3
    RESERVED = 4

    @classmethod
    def _missing_(cls, value):
        if 4 <= value <= 127:
            return FunctionBlockClassAuxiliary.RESERVED
        else:
            raise ValueError()


class FunctionBlockClassAlert(FunctionBlockClass):
    RESERVED = 1

    @classmethod
    def _missing_(cls, value):
        if 1 <= value <= 127:
            return FunctionBlockClassAlert.RESERVED
        else:
            raise ValueError()


FUNCTION_BLOCK_CLASSENUM_BY_PARENT = {
    FunctionBlockParentClass.INPUT: FunctionBlockClassInput,
    FunctionBlockParentClass.OUTPUT: FunctionBlockClassOutput,
    FunctionBlockParentClass.CONTROL: FunctionBlockClassControl,
    FunctionBlockParentClass.ADVANCED_CONTROL: FunctionBlockClassAdvancedControl,
    FunctionBlockParentClass.CALCULATION: FunctionBlockClassCalculation,
    FunctionBlockParentClass.AUXILIARY: FunctionBlockClassAuxiliary,
    FunctionBlockParentClass.ALERT: FunctionBlockClassAlert
}
