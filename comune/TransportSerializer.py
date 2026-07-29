import asyncio
import struct

from comune.PacketType import PacketType as PacketType
HEADER_FORMAT = "!BI"  # ! = little endian , B = Byte ,  I = Integer
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)
PAYLOAD_SIZE = 5

# dupa aceasta functie trebuie musai folosit GetPacketContent,
# intrucat avem deja citit de pe reader headerul, atentie mare


async def ReadPacket(reader: asyncio.StreamReader):
    try:
        header = await reader.read(HEADER_SIZE)
        if header.__len__()<PAYLOAD_SIZE:
            print(f"probleme la {header} cu dimensiunea {header.__len__()}")
            return 0,0
        typep, length = struct.unpack(HEADER_FORMAT, header)
        payload = await reader.readexactly(int(length))
        return typep, payload
    except (ConnectionError, ConnectionResetError, asyncio.IncompleteReadError) as e:
        print(f"probleme la {e}")
        print("trebuie deconectat 2")
        print()
        print()
        exit()


async def GetPacketContent(reader:asyncio.StreamReader, dim:int) -> bytes:
    content = await reader.readexactly(dim)
    # aparent .drain() funcitoneaza doar pentru scriere, in rest nu si are locul
    # await content.drain()
    return content


async def ReadPacketTypeAndLength(reader: asyncio.StreamReader) :
    if reader.at_eof():
        print("reader e gol, trebuie sa incheiem conexiunea")
    try:
        header = await reader.read(HEADER_SIZE)
        if header.__len__()<PAYLOAD_SIZE:
            print(f"probleme la {header} cu dimensiunea {header.__len__()}")
            return 0,0
        typep, lenght = struct.unpack(HEADER_FORMAT, header)
        return typep, lenght
    except (ConnectionError, ConnectionResetError, asyncio.IncompleteReadError) as e:
        # print(f"probleme la {e}")
        # print("trebuie deconectat 3")
        print()
        print()
        return PacketType.DISCONNECT, 0



async def WritePacket(writer: asyncio.StreamWriter,
                       messageType: PacketType,
                       payload: bytes):
    if payload is not None:
        header = struct.pack(HEADER_FORMAT, int(messageType), len(payload))
        writer.write(header + payload)
    else:
        header = struct.pack(HEADER_FORMAT, int(messageType), 0)
        writer.write(header)
    await writer.drain()