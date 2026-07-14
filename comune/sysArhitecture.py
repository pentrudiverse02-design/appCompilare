from enum import IntEnum


class SystemArchitecture(IntEnum):
    x86_64 = 1
    arm64 = 2
    aarch_64 = 3
def SystemArchitectureConvStr(string):
    match string:
        case 'x86_64' : return SystemArchitecture(1)
        case "arm64" : return SystemArchitecture(2)
        case "aarch_64":  return SystemArchitecture(3)
    return None