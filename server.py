import asyncio
import json
import os.path
import struct

from Package import *
from PackageType import *


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
            os.makedirs("AppCompilareServerDir")
            os.makedirs("AppCompilareServerDir/ascunse")
        async with self.SERVER:
            await self.SERVER.serve_forever()

    async def ClientConnect(self, addr, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    # aici o sa pun noua implementare din Package
        # header = await reader.readexactly(Package.HEADER_SIZE)
        # mestype, lungimeData = struct.unpack(HEADER_FORMAT, header)
        packtype , packlen = ReadPackageHeader(reader)
    # aici am modificat pentru packageType
        if packtype != PackageType.LOGIN_CREDENTIALS:
            s = f"draga {addr}, trimite mi creditentialele tale".encode('utf-8')
            #await Package.WritePackage(writer, Package.PackageType.GET_ERRORS, s)
            await WritePackage(writer, PackageType.GET_ERRORS, s)
            return
        data = await ReadPackageContent(reader).decode('utf-8')
        # data = await reader.readexactly(lungimeData)
        # data = json.loads(data.decode('utf-8'))
        self.clients[addr] = {"readerPipe": reader,
                              "writerPipe": writer,
                              "request": data}
        if addr in self.clients.keys():
            s = f"am primit de la tine {addr} datele {self.clients[addr]}"
            print(s)
            print(self.clients[addr]["request"])
            if self.clients[addr]["request"]["stay"] == False:
                # facem in ascunse
                self.clients[addr]["request"]["folderloc"] = "AppCompilareServerDir/ascunse/" + \
                                                             self.clients[addr]["request"]["folderloc"]
            else:
                self.clients[addr]["request"]["folderloc"] = "AppCompilareServerDir/" + self.clients[addr]["request"][
                    "folderloc"]
            if not os.path.exists(self.clients[addr]["request"]["folderloc"]):
                os.makedirs(self.clients[addr]["request"]["folderloc"])
            await WritePackage(self.clients[addr]["writerPipe"],
                                       PackageType.STATUS,
                                       "ok".encode('utf-8'))


    async def ClientHandle(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        # if not self.clients.__contains__(writer.get_extra_info('peername')):
        #     await self.ClientConnect(writer.get_extra_info('peername'), reader,writer)
        while True:
            client = writer.get_extra_info('peername')
            if not client in self.clients.keys():
                await self.ClientConnect(writer.get_extra_info('peername'), reader, writer)
        ## toate comment urile de mai jos sunt pentru a citi tipul de packet, redundant
            # try:
            #     header = await reader.readexactly(Package.HEADER_SIZE)
            # except (ConnectionError, ConnectionResetError, asyncio.IncompleteReadError) as e:
            #     print(f"probleme la conexiune {e}")
            #     break
            # header, length = struct.unpack(Package.HEADER_FORMAT, header)
            try:
                header= ReadPackagetType(reader)
            except (ConnectionError, ConnectionResetError, asyncio.IncompleteReadError) as e:
                print(f"probleme la {e}")
                print("trebuie deconectat")
                break
            match header:
                case PackageType.UPLOAD_ZIP:
                    await self.ReceiveZip(client)
                case PackageType.GET_ERRORS:
                    await self.ReceiveErrors(client)
                case PackageType.DISCONNECT:
                    await self.Disconnect(client)

    async def ReceiveZip(self, client):
        stream = self.clients[client]["readerPipe"]
        for i in self.clients[client]["request"]["expected"]:
            s = self.clients[client]["request"]["folderloc"] + '/' + i
            print(s)
            file = open(s, 'wb')
            #while True:
            dim = int(self.clients[client]["request"]["expected"][i])
            continut = await stream.readexactly(dim)
            await continut.drain()
            ##continut=continut.decode('utf-8')
            file.write(continut)
            break
            #aici o sa doresc sa-l despachetez

    async def ReceiveErrors(self, client):
        pass

    async def Disconnect(self, client):
        pass


a = Server()