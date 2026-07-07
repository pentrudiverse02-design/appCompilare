import asyncio
import json
import os.path
import struct

import Package
from Package import HEADER_FORMAT


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
        self.SERVER = await asyncio.start_server(self.ClientHandle, self.server_host, self.server_port)
        addrs = ', '.join(str(sock.getsockname()) for sock in self.SERVER.sockets)
        print(f'Serving on {addrs}')
        if not os.path.exists("AppCompilareServerDir"):
            os.makedirs("AppCompilareServerDir",mode=0o777)
            os.makedirs("AppCompilareServerDir/ascunse")
        async with self.SERVER:
            await self.SERVER.serve_forever()

    async def ClientConnect(self, addr, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        header = await reader.readexactly(Package.HEADER_SIZE)
        mestype, lungimeData = struct.unpack(HEADER_FORMAT, header)
        if mestype != Package.PackageType.LOGIN_CREDENTIALS:
            s = f"draga {addr}, trimite mi creditentialele tale".encode('utf-8')
            await Package.WritePackage(writer, Package.PackageType.GET_ERRORS, s)
            return
        data = await reader.readexactly(lungimeData)
        data = json.loads(data.decode('utf-8'))
        self.clients[addr] = {"readerPipe": reader,
                              "writerPipe": writer,
                              "request": data}
        if addr in self.clients.keys():
            s = f"am primit de la tine {addr} datele {self.clients[addr]}".encode('utf-8')
            print(s)
            print(self.clients[addr]["request"])
            if self.clients[addr]["request"]["stay"] is False:
                #facem in ascunse
                if not os.path.exists( "AppCompilareServerDir/ascunse/"+self.clients[addr]["request"]["folderloc"] ):
                    os.makedirs("AppCompilareServerDir/ascunse/"+self.clients[addr]["request"]["folderloc"])
            else:
                if not os.path.exists("AppCompilareServerDir/" + self.clients[addr]["request"]["folderloc"]):
                    os.makedirs("AppCompilareServerDir/" + self.clients[addr]["request"]["folderloc"])

            await Package.WritePackage(self.clients[addr]["writerPipe"],
                                       Package.PackageType.STATUS,
                                       "ok".encode('utf-8'))

    # aici as vrea sa aflu cum pot sa fac o corutina sa fie intr un loop care ruleaza permanent, pana la oprire explicita
    # doresc sa fac o intrerupere pentru momentul in care o teava de read primeste ceva
    # insa nu am idee cum si nici nu am gasit altceva inafara de while True
    async def ClientHandle(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        # if not self.clients.__contains__(writer.get_extra_info('peername')):
        #     await self.ClientConnect(writer.get_extra_info('peername'), reader,writer)
        while True:
            client = writer.get_extra_info('peername')
            if not client in self.clients.keys():
                await self.ClientConnect(writer.get_extra_info('peername'), reader, writer)
            header = await reader.readexactly(Package.HEADER_SIZE)
            match header:
                case Package.PackageType.UPLOAD_ZIP:
                    await self.ReceiveZip(client)

                case Package.PackageType.GET_ERRORS:
                    await self.ReceiveErrors(client)
                case Package.PackageType.DISCONNECT:
                    await self.Disconnect(client)



    async def ReceiveZip(self, client):
        s=asyncio.StreamReader
        stream=self.clients[client]["readerPipe"]
        for i in self.clients[client]["request"]["expected"]:
            file = open(i)
            while True:
                stream.readexactly()

    async def ReceiveErrors(self, client):
        pass

    async def Disconnect(self, client):
        pass


a = Server()
