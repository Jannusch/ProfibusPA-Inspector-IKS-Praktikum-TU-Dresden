from enum import IntEnum
from Block import Block


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


class TransducerBlockClass(IntEnum):
    pass


class TransducerBlockClassPressure(TransducerBlockClass):
    DIFFERENTIAL = 1
    ABSOLUTE = 2
    GAGE = 3
    PRESSURE_LEVEL_FLOW = 4
    PRESSURE_LEVEL = 5
    PRESSURE_FLOW = 6
    MIXED_PRESSURE = 7


class TransducerBlockClassTemperature(TransducerBlockClass):
    THERMOCOUPLE = 1
    TC = 1
    RESISTANCE_THERMOMETER = 2
    RTD = 2
    PYROMETER = 3
    TC_DC = 16
    RTD_R = 17
    TC_RTD_R_DC = 18


class TransducerBlockClassFlow(TransducerBlockClass):
    ELECTROMAGNETIC = 1
    VORTEX = 2
    CORIOLIS = 3
    THERMAL_MASS = 4
    ULTRASONIC = 5
    VARIABLE_AREA = 6
    DIFFERENTIAL_PRESSURE = 7


class TransducerBlockClassLevel(TransducerBlockClass):
    HYDROSTATIC = 1
    ECHO_LEVEL = 2
    RADIOMETRIC = 3
    CAPACITY = 4


class TransducerBlockClassActuator(TransducerBlockClass):
    ELECTRIC = 1
    ELECTRO_PNEUMATIC = 2
    ELECTRO_HYDRAULIC = 3


class TransducerBlockClassDiscreteIO(TransducerBlockClass):
    SENSOR_INPUT = 1
    ACTUATOR = 2


class TransducerBlockClassAnalyser(TransducerBlockClass):
    STANDARD = 1


class TransducerBlockClassAuxiliary(TransducerBlockClass):
    TRANSFER = 1
    CONTROL = 2
    LIMIT = 3


class TransducerBlockClassAlarm(TransducerBlockClass):
    BINARY_MESSAGE = 1


TRANSDUCER_BLOCK_CLASSENUM_BY_PARENT = {
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
