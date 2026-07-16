from enum import IntEnum


class PacketType(IntEnum):
    LOGIN_CREDENTIALS = 0
    ZIP = 1
    GET_LOGS = 2
    STATUS = 3
    SELECTED_ZIPS = 4  # it will be used to receive the {"fileName":fileSize,...} for zips
    DISCONNECT = 5
    ERROR = 6