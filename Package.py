import asyncio
import struct
from PackageType import PackageType as PackageType

HEADER_FORMAT = "!BI"  # ! = little endian , B = Byte ,  I = Integer
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)
PAYLOAD_SIZE = 1024

async def ReadPackageHeader(reader: asyncio.StreamReader ) :
    header = await reader.read(HEADER_SIZE)
    typep, lenght = struct.unpack(HEADER_FORMAT, header)
    typep=typep.decode('utf-8') #intrucat am avut niste probleme fac decode de dragul lui
    payload = await reader.readexactly(lenght.decode('utf-8'))
    return typep,payload


async def ReadPackageContent(reader: asyncio.StreamReader) -> bytes:
    a,b= await ReadPackageHeader(reader)
    content = await reader.readexactly(int(b))
    # aparent .drain() funcitoneaza doar pentru scriere, in rest nu si are locul
    # await content.drain()
    return content


async def ReadPackagetType(reader: asyncio.StreamReader )-> PackageType:
    header = await reader.read(HEADER_SIZE)
    typep, lenght = struct.unpack(HEADER_FORMAT, header)
    #return  typep.decode('utf-8')
    #aici nu cred ca e nevoie de decode, unpack face decodarea in format target
    return typep


async def GetPackageSize(reader: asyncio.StreamReader ) -> int:
    header = await reader.readexactly(HEADER_SIZE)
    typep, lenght = struct.unpack(HEADER_FORMAT, header)
    # return  int(lenght.decode('utf-8'))
    #si aici ca ma sus
    return int(lenght)


async def WritePackage(writer: asyncio.StreamWriter,
                       messageType: PackageType,
                       payload: bytes):
    header = struct.pack(HEADER_FORMAT, int(messageType), len(payload))
    writer.write(header + payload)
    await writer.drain()