from enum import IntEnum


class CompilationType(IntEnum):
    RELEASE = 1
    DEBUG = 2
    LIBRARY = 3
def CompilationTypeConvStr(string):
    match string:
        case "RELEASE": return CompilationType(1)
        case "DEBUG ": return CompilationType(2)
        case "LIBRARY": return CompilationType(3)
    return None