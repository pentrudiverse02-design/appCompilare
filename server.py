import asyncio
import json
import struct

import Package
from Package import HEADER_FORMAT


class Server:
    clients={}
    server_host = '127.0.0.1' 
    server_port = 8008
    folderServer = ''
    maxConnections = 0
    SERVER=None
    def __init__(self):
        asyncio.run(self.CreateServer())
    async def CreateServer(self):
        self.SERVER = await asyncio.start_server(self.ClientHandle,self.server_host,self.server_port)
        addrs = ', '.join(str(sock.getsockname()) for sock in self.SERVER.sockets)
        print(f'Serving on {addrs}')
        async with self.SERVER:
            await self.SERVER.serve_forever()

    async def ClientConnect(self,addr,reader:asyncio.StreamReader,writer:asyncio.StreamWriter):
        header = await reader.read(Package.HEADER_SIZE)
        mestype, lungimeData= struct.unpack(HEADER_FORMAT,header)
        if mestype is not Package.PackageType.LOGIN_CREDENTIALS:
            writer.write(f"draga {addr}, trimite mi creditentialele tale".encode('utf-8'))
            await writer.drain()
            return
        data = await reader.readexactly(lungimeData)
        data = json.loads( data.decode('utf-8'))
        self.clients[addr]={"readerPipe":reader,
                            "writerPipe":writer,
                            "request":data}
        if self.clients.__contains__(addr):
            writer.write(f"am primit de la tine {addr} datele {self.clients[addr]}".encode('utf-8'))
            await writer.drain()


    async def ClientHandle(self,reader:asyncio.StreamReader,writer:asyncio.StreamWriter):
        if not self.clients.__contains__(writer.get_extra_info('peername')):
            await self.ClientConnect(writer.get_extra_info('peername'), reader,writer)

        # data = await reader.read(1024)
        # message = data.decode('utf-8')
        # addr = writer.get_extra_info('peername')
        # print(f"am primit {message} de la {addr}")
        # self.clients[addr]=message
        # writer.write("ok".encode('utf-8'))
        # await writer.drain()

while True:
    a=Server()
