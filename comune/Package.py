import asyncio
import struct

from comune.PackageType import PackageType
HEADER_FORMAT = "!BI"  # ! = little endian , B = Byte ,  I = Integer
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)
PAYLOAD_SIZE = 1024


async def ReadPackageHeader(reader: asyncio.StreamReader):
    try:
        header = await reader.read(HEADER_SIZE)
        typep, length = struct.unpack(HEADER_FORMAT, header)
        return typep, length
    except (ConnectionError, ConnectionResetError, asyncio.IncompleteReadError) as e:
        print(f"probleme la {e}")
        print("trebuie deconectat")
        exit()

# dupa aceasta functie trebuie musai folosit GetPackageContent,
# intrucat avem deja citit de pe reader headerul, atentie mare


async def ReadPackage(reader: asyncio.StreamReader):
    try:
        header = await reader.read(HEADER_SIZE)
        typep, length = struct.unpack(HEADER_FORMAT, header)
        payload = await reader.readexactly(int(length))
        return typep, payload
    except (ConnectionError, ConnectionResetError, asyncio.IncompleteReadError) as e:
        print(f"probleme la {e}")
        print("trebuie deconectat")
        exit()


async def GetPackageContent(reader:asyncio.StreamReader, dim:int) -> bytes:
    content = await reader.readexactly(dim)
    # aparent .drain() funcitoneaza doar pentru scriere, in rest nu si are locul
    # await content.drain()
    return content


async def ReadPackagetTypeAndLength(reader: asyncio.StreamReader) :
    if reader.at_eof():
        print("reader e gol, trebuie sa incheiem conexiunea")
    try:
        header = await reader.read(HEADER_SIZE)
        typep, lenght = struct.unpack(HEADER_FORMAT, header)
        return typep, lenght
    except (ConnectionError, ConnectionResetError, asyncio.IncompleteReadError) as e:
        print(f"probleme la {e}")
        print("trebuie deconectat")
        exit()


async def WritePackage(writer: asyncio.StreamWriter,
                       messageType: PackageType,
                       payload: bytes):
    header = struct.pack(HEADER_FORMAT, int(messageType), len(payload))
    writer.write(header + payload)
    await writer.drain()