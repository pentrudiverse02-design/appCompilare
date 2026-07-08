import asyncio
import struct
from PackageType import PackageType as PackageType

HEADER_FORMAT = "!BI"  # ! = little endian , B = Byte ,  I = Integer
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)
PAYLOAD_SIZE = 1024

class Package:
    @staticmethod
    async def ReadPackage(reader: asyncio.StreamReader ) :
        header = await reader.read(HEADER_SIZE)
        typep, lenght = struct.unpack(HEADER_FORMAT, header)
        typep=typep.decode('utf-8') #intrucat am avut niste probleme fac decode de dragul lui
        payload = await reader.readexactly(lenght.decode('utf-8'))
        return typep,payload
    @staticmethod
    async def ReadPackageContent(reader: asyncio.StreamReader) -> bytes:
        a,b= await Package.ReadPackage(reader)
        return b
    @staticmethod
    async def ReadPackagetType(reader: asyncio.StreamReader )-> PackageType:
        header = await reader.read(HEADER_SIZE)
        typep, lenght = struct.unpack(HEADER_FORMAT, header)
        return  typep.decode('utf-8')
    @staticmethod
    async def GetPackageSize(reader: asyncio.StreamReader ) -> int:
        header = await reader.readexactly(HEADER_SIZE)
        typep, lenght = struct.unpack(HEADER_FORMAT, header)
        return  int(lenght.decode('utf-8'))
    @staticmethod
    async def WritePackage(writer: asyncio.StreamWriter,
                           messageType: PackageType,
                           payload: bytes):
        header = struct.pack(HEADER_FORMAT, int(messageType), len(payload))
        writer.write(header + payload)
        await writer.drain()