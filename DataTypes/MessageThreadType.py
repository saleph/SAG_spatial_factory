from enum import IntEnum


class MessageThreadType(IntEnum):
    Unknown = 0,
    RootComponentProduction = 1,
    ResourceInfo = 2,
    KeepAlive = 3