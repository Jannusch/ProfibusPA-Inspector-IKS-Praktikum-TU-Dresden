from enum import IntEnum
from GenericBlock import GenericBlock


class TransducerBlockParentClass(IntEnum):
    PRESSURE = 1
    TEMPERATURE = 2
    FLOW = 3
    LEVEL = 4
    ACTUATOR = 5
    DISCRETE_IO = 6
    ANALYSER = 7
    AUXILIARY = 8
    ALARM = 9
    RESERVED = 10

    @classmethod
    def _missing_(cls, value):
        if 10 <= value <= 127:
            return TransducerBlockParentClass.RESERVED
        else:
            raise ValueError()


class TransducerBlockClass(IntEnum):
    pass


class TransducerBlock(GenericBlock):

    def __init__(self, bytz):
        super(bytz)

        if self.block_object_byte != 1:
            raise ValueError("Block Object must be 0x03 in Transducer Block! (got {})".format(self.block_object_byte))

        self.use_class_definition = {
            TransducerBlockParentClass.PRESSURE: TransducerBlockClassPressure,
            TransducerBlockParentClass.TEMPERATURE: TransducerBlockClassTemperature,
            TransducerBlockParentClass.FLOW: TransducerBlockClassFlow,
            TransducerBlockParentClass.LEVEL: TransducerBlockClassLevel,
            TransducerBlockParentClass.ACTUATOR: TransducerBlockClassActuator,
            TransducerBlockParentClass.DISCRETE_IO: TransducerBlockClassDiscreteIO,
            TransducerBlockParentClass.ANALYSER: TransducerBlockClassAnalyser,
            TransducerBlockParentClass.AUXILIARY: TransducerBlockClassAuxiliary,
            TransducerBlockParentClass.ALARM: TransducerBlockClassAlarm
        }

    def get_class(self) -> TransducerBlockClass:
        enum = self.use_class_definition[TransducerBlockParentClass(
            self.parent_class_byte)]
        if enum != None:
            return enum(self.class_byte)
        else:
            return None

    def get_parent_class(self) -> TransducerBlockParentClass:
        return TransducerBlockParentClass(self.parent_class_byte)


class TransducerBlockClassPressure(TransducerBlockClass):
    DIFFERENTIAL = 1
    ABSOLUTE = 2
    GAGE = 3
    PRESSURE_LEVEL_FLOW = 4
    PRESSURE_LEVEL = 5
    PRESSURE_FLOW = 6
    MIXED_PRESSURE = 7
    RESERVED = 8

    @classmethod
    def _missing_(cls, value):
        if 8 <= value <= 127:
            return TransducerBlockClassPressure.RESERVED
        else:
            raise ValueError()


class TransducerBlockClassTemperature(TransducerBlockClass):
    THERMOCOUPLE = 1
    TC = 1
    RESISTANCE_THERMOMETER = 2
    RTD = 2
    PYROMETER = 3
    RESERVED = 4
    TC_DC = 16
    RTD_R = 17
    TC_RTD_R_DC = 18

    @classmethod
    def _missing_(cls, value):
        if 4 <= value <= 15 or 19 <= value <= 127:
            return TransducerBlockClassTemperature.RESERVED
        else:
            raise ValueError()


class TransducerBlockClassFlow(TransducerBlockClass):
    ELECTROMAGNETIC = 1
    VORTEX = 2
    CORIOLIS = 3
    THERMAL_MASS = 4
    ULTRASONIC = 5
    VARIABLE_AREA = 6
    DIFFERENTIAL_PRESSURE = 7
    RESERVED = 8

    @classmethod
    def _missing_(cls, value):
        if 8 <= value <= 127:
            return TransducerBlockClassFlow.RESERVED
        else:
            raise ValueError()


class TransducerBlockClassLevel(TransducerBlockClass):
    HYDROSTATIC = 1
    ECHO_LEVEL = 2
    RADIOMETRIC = 3
    CAPACITY = 4
    RESERVED = 5

    @classmethod
    def _missing_(cls, value):
        if 5 <= value <= 127:
            return TransducerBlockClassLevel.RESERVED
        else:
            raise ValueError()


class TransducerBlockClassActuator(TransducerBlockClass):
    ELECTRIC = 1
    ELECTRO_PNEUMATIC = 2
    ELECTRO_HYDRAULIC = 3
    RESERVED = 4

    @classmethod
    def _missing_(cls, value):
        if 4 <= value <= 127:
            return TransducerBlockClassActuator.RESERVED
        else:
            raise ValueError()


class TransducerBlockClassDiscreteIO(TransducerBlockClass):
    SENSOR_INPUT = 1
    ACTUATOR = 2
    RESERVED = 3

    @classmethod
    def _missing_(cls, value):
        if 3 <= value <= 127:
            return TransducerBlockClassDiscreteIO.RESERVED
        else:
            raise ValueError()


class TransducerBlockClassAnalyser(TransducerBlockClass):
    STANDARD = 1
    RESERVED = 2

    @classmethod
    def _missing_(cls, value):
        if 2 <= value <= 127:
            return TransducerBlockClassAnalyser.RESERVED
        else:
            raise ValueError()


class TransducerBlockClassAuxiliary(TransducerBlockClass):
    TRANSFER = 1
    CONTROL = 2
    LIMIT = 3
    RESERVED = 4

    @classmethod
    def _missing_(cls, value):
        if 4 <= value <= 127:
            return TransducerBlockClassAuxiliary.RESERVED
        else:
            raise ValueError()


class TransducerBlockClassAlarm(TransducerBlockClass):
    BINARY_MESSAGE = 1
    RESERVED = 2

    @classmethod
    def _missing_(cls, value):
        if 2 <= value <= 127:
            return TransducerBlockClassAlarm.RESERVED
        else:
            raise ValueError()
