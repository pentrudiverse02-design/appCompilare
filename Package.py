import asyncio
import struct
from PackageType import PackageType as PackageType

HEADER_FORMAT = "!BI"  # ! = little endian , B = Byte ,  I = Integer
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)
PAYLOAD_SIZE = 1024


async def ReadPackageHeader(reader: asyncio.StreamReader):
    header = await reader.read(HEADER_SIZE)
    typep, lenght = struct.unpack(HEADER_FORMAT, header)
    return typep, lenght


async def ReadPackage(reader: asyncio.StreamReader):
    try:
        header = await reader.read(HEADER_SIZE)
    except (ConnectionError, ConnectionResetError, asyncio.IncompleteReadError) as e:
        print(f"probleme la {e}")
        print("trebuie deconectat")
        exit("nu am citit ceva bine")
    typep, lenght = struct.unpack(HEADER_FORMAT, header)
    payload = await reader.readexactly(int(lenght))
    return typep, payload


async def ReadPackageContent(reader: asyncio.StreamReader) -> bytes:
    try:
        a, b = await ReadPackageHeader(reader)
    except (ConnectionError, ConnectionResetError, asyncio.IncompleteReadError) as e:
        print(f"probleme la {e}")
        print("trebuie deconectat")
        exit("nu am citit ceva bine")
    content = await reader.readexactly(int(b))
    # aparent .drain() funcitoneaza doar pentru scriere, in rest nu si are locul
    # await content.drain()
    return content


async def ReadPackagetType(reader: asyncio.StreamReader) -> PackageType:
    try:
        header = await reader.read(HEADER_SIZE)
    except (ConnectionError, ConnectionResetError, asyncio.IncompleteReadError) as e:
        print(f"probleme la {e}")
        print("trebuie deconectat")
        exit("nu am citit ceva bine")
    typep, lenght = struct.unpack(HEADER_FORMAT, header)
    # return  typep.decode('utf-8')
    # aici nu cred ca e nevoie de decode, unpack face decodarea in format target
    return typep


async def GetPackageSize(reader: asyncio.StreamReader) -> int:
    try:
        header = await reader.readexactly(HEADER_SIZE)
    except (ConnectionError, ConnectionResetError, asyncio.IncompleteReadError) as e:
        print(f"probleme la {e}")
        print("trebuie deconectat")
        exit("nu am citit ceva bine")
    typep, lenght = struct.unpack(HEADER_FORMAT, header)
    # return  int(lenght.decode('utf-8'))
    # si aici ca ma sus
    return int(lenght)


async def WritePackage(writer: asyncio.StreamWriter,
                       messageType: PackageType,
                       payload: bytes):
    header = struct.pack(HEADER_FORMAT, int(messageType), len(payload))
    writer.write(header + payload)
    await writer.drain()
