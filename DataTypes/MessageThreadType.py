from enum import IntEnum


class MessageThreadType(IntEnum):
    Unknown = 0,
    CarProduction = 1,
    ResourceInfo = 2,
    KeepAlive = 3