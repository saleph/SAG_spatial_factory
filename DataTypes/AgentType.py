from enum import Enum


class AgentType(Enum):
    UNKNOWN = -1,
    STORAGE = 0,
    CAR = 1,
    WHEEL = 2,
    DOOR = 3,
    ENGINE = 4
