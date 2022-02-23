from enum import Enum, IntEnum


class Type(Enum):
    DEFAULT_MODE = 0
    SERVICE_MODE = 1
    PREPARE_MODE = 2
    DETECTOR_MODE = 3

class Modes(IntEnum):
    Gamma_1 = 0
    Gamma_2 = 1
    Gamma_3 = 2
    Gamma_4 = 4
    Gamma_5 = 3
