from enum import IntEnum


class PackageType(IntEnum):
    LOGIN_CREDENTIALS = 0
    UPLOAD_ZIP = 1
    GET_LOGS = 2
    STATUS = 3
    DOWNLOAD_ZIP = 4
    RESULT = 5
    DISCONNECT = 6
    ERROR = 7