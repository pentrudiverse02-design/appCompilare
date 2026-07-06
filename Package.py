import asyncio
import struct
from enum import IntEnum


class PackageType(IntEnum):
    LOGIN_CREDENTIALS = 0
    UPLOAD_ZIP = 1
    GET_LOGS = 2
    STATUS = 3
    GET_ERRORS = 4
    RESULT = 5
HEADER_FORMAT = "!BI" # ! = little endian , B = Byte ,  I = Integer
HEADER_SIZE= struct.calcsize(HEADER_FORMAT)

async def ReadPackage(reader: asyncio.StreamReader):
    header = await reader.read(HEADER_SIZE)
    typep, lenght = struct.unpack(HEADER_FORMAT,header)
    payload = await reader.readexactly(lenght)
    return typep, payload
async def PrintMessage(reader: asyncio.StreamReader):
    typep, payload= ReadPackage(reader)
    print(typep)
    print(payload.decode('utf-8'))
async def WritePackage(writer : asyncio.StreamWriter,
                       messageType : PackageType,
                       payload : bytes):
    header = struct.pack(HEADER_FORMAT, int(messageType),len(payload))
    writer.write(header + payload)
    await writer.drain()