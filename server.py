import asyncio
import json
import os.path
import struct

from Package import *
from PackageType import *
from zips import ZipClass


class Server:
    clients = {}
    server_host = '127.0.0.1'
    server_port = 8008
    folderServer = ''
    maxConnections = 0
    SERVER = None

    def __init__(self):
        asyncio.run(self.CreateServer())

    async def CreateServer(self):
        self.SERVER = await asyncio.start_server(self.ReceiveStreamHandle, self.server_host, self.server_port)
        addrs = ', '.join(str(sock.getsockname()) for sock in self.SERVER.sockets)
        print(f'Serving on {addrs}')
        if not os.path.exists(self.folderServer + "AppCompilareServerDir"):
            os.makedirs(self.folderServer + "AppCompilareServerDir")
            os.makedirs(self.folderServer + "AppCompilareServerDir/ascunse")
        async with self.SERVER:
            await self.SERVER.serve_forever()


    async def ClientConnect(self, addr, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        packtype, payload = await ReadPackage(reader)
        if packtype != PackageType.LOGIN_CREDENTIALS:
            s = f"draga {addr}, trimite mi creditentialele tale".encode('utf-8')
            await WritePackage(writer, PackageType.ERROR, s)
            return
        client = json.loads(payload.decode('utf-8'))
        client["reader"] = reader
        client["writer"] = writer
        self.clients[addr] = client
        if addr not in self.clients.keys():
            print("nu l am pus in server.clients")
            print(f"a pocnit din server ClientConnect la utilizator:{addr}")
            exit()
        if not self.clients[addr]["stay"]:
            locationComplition = "AppCompilareServerDir/ascunse/"
        else:
            locationComplition = "AppCompilareServerDir/"
        self.clients[addr]["folder"] = (self.folderServer +
                                        locationComplition +
                                        str(addr))
        if not os.path.exists(self.clients[addr]["folder"]):
            os.makedirs(self.clients[addr]["folder"])
        self.clients[addr]["zip"]=ZipClass(writer,reader,self.clients[addr]["folder"])
        await WritePackage(self.clients[addr]["writer"],
                           PackageType.STATUS,
                           "ok".encode('utf-8'))
        print(f"am primit de la tine {addr} datele {self.clients[addr]}")

    async def ReceiveStreamHandle(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        while True:
            # if reader.at_eof():
            #     print("sunt la client, conectiune inchisa")
            #     exit()
            client = writer.get_extra_info('peername')
            if not client in self.clients.keys():
                await self.ClientConnect(writer.get_extra_info('peername'), reader, writer)
                continue
            header, lenght = await ReadPackagetTypeAndLength(reader)
            match header:
                case PackageType.ZIP:
                    await self.ReceiveZip(client)
                case PackageType.ERROR:
                    pass
                case PackageType.SELECTED_ZIPS:
                    payload = await GetPackageContent(reader, lenght)
                    payload = payload.decode('utf-8')
                    print(payload)
                    self.clients[client]["zip"].ZipsToReceive(payload)
                    #ZipToReceive(json.loads(payload.decode('utf-8')))
                case PackageType.DISCONNECT:
                    pass


    async def ReceiveZip(self, client):
        await self.clients[client]["zip"].GetZip()


a = Server()
