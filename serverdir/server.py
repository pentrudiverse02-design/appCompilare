import json
import os

from pathlib import Path
from zipfile import ZipFile, BadZipFile

from comune.TransportSerializer import *
from comune.zips import ZipClass


class Server:
    clients = {}
    server_host = '127.0.0.1'
    server_port = 8008
    folderServer = 'serverdir/'
    maxConnections = 0
    SERVER = None

    def __init__(self, port=8008):
        self.server_port = port
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
        packtype, payload = await ReadPacket(reader)
        if packtype != PacketType.LOGIN_CREDENTIALS:
            s = f"draga {addr}, trimite mi creditentialele tale".encode('utf-8')
            await WritePacket(writer, PacketType.ERROR, s)
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
                                        self.clients[addr]["folder"])
        if not os.path.exists(self.clients[addr]["folder"]):
            os.makedirs(self.clients[addr]["folder"])
        self.clients[addr]["zip"] = ZipClass(writer, reader, self.clients[addr]["folder"])
        await WritePacket(self.clients[addr]["writer"],
                          PacketType.STATUS,
                          "ok".encode('utf-8'))
        print(f"am primit de la tine {addr} datele {self.clients[addr]["compileFor"]}  "
              f"{self.clients[addr]["sysArchi"]}  "
              f"{self.clients[addr]["folder"]}   "
              f"{self.clients[addr]["stay"]}" )

    # probabil o sa trebuiasca sa implementez la fiecare metoda din clasa de mesagerie un
    # return True False
    # in caz de succes sau nu.
    # in caz de esec sa se apeleze Disconnect(client)
    async def ReceiveStreamHandle(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        while True:
            client = writer.get_extra_info('peername')
            if not client in self.clients.keys():
                await self.ClientConnect(writer.get_extra_info('peername'), reader, writer)
                continue
            header, lenght = await ReadPacketTypeAndLength(reader)
            match header:
                case PacketType.ZIP:
                    print(f"apelez metoda de receptie zips de la {client}")
                    await self.ReceiveZip(client)
                    await self.UnpackAndCompile(client,writer)
                    await WritePacket(writer,PacketType.DISCONNECT,bytes())
                case PacketType.ERROR:
                    print("a fost detectata o eroare de tipul")
                    await self.DisconnectClient(client)
                    break
                case PacketType.SELECTED_ZIPS:
                    payload = await GetPacketContent(reader, lenght)
                    payload = json.loads(payload.decode('utf-8'))
                    print(f"o sa primesc: {type(payload)} si {payload}")
                    self.clients[client]["zip"].ZipsToReceive(payload)
                    # ZipToReceive(json.loads(payload.decode('utf-8')))
                case PacketType.DISCONNECT:
                    await self.DisconnectClient(client)
                    break

    async def ReceiveZip(self, client):
        await self.clients[client]["zip"].GetZip()

    async def DisconnectClient(self, client):
        # verificam daca putem sa stergem clientul
        if self.clients.keys().__contains__(client):
            # if self.clients[client]["stay"] is False:
            #     os.removedirs("AppCompilareServerDir/ascunse/" + str(self.clients[str(client)]))
            self.clients.pop(client)

    # aici o sa trebuiasca sa iteram lista de fisiere .zip ale clientului
    # odata ce dezarhivam un folder, intram in el, vedem ce comtine, si apelam direct Makefile ul


    async def UnpackAndCompile(self, client,writer: asyncio.StreamWriter):
        p = Path(self.clients[client]['folder'])
        lista=[]
        for c in p.glob("*.zip"):
            lista.append(c)
        print("-------")
        print()
        print(lista)
        print()
        print("!!!!!!!!!!!")
        for child in lista:
            if not child.is_file():
                print("ce MA?")
                continue
            try:
                with ZipFile(child, 'r') as zips:
                    zips.extractall(p)
                    patttt=child.parent/child.stem
                    print(patttt)
                    c = list(patttt.glob("*.c"))
                    cpp = list(patttt.glob("*.cpp"))
                    if c:
                        filetype="cExe"
                    elif cpp:
                        filetype="cppExe"
                    command=(f'echo ""'
                             f'echo "----------------- APELEZ SHELL DIN PYTHON ----------------" ;'
                             f' pwd; '
                             f" cd {patttt} ;pwd ; ls ; "
                             f" ARCHITECTURE={self.clients[client]["sysArchi"]} ; "
                             f" make -f ~/app_compilare/appCompilare/serverdir/Makefile {filetype} ;"
                             f'echo "\n---------------- AM TERMINAT APELUL DIN PYTHON -----------------" ;'
                             f'echo ""')
                    C = await asyncio.create_subprocess_shell(command,
                                                              stdout=asyncio.subprocess.PIPE,
                                                              stderr=asyncio.subprocess.STDOUT
                                                              )
                    try:
                        stdoutt, _ = await asyncio.wait_for(C.communicate(), timeout=120)
                        await WritePacket(writer,PacketType.STATUS,stdoutt)
                        print(stdoutt.decode(errors="replace"))
                    except asyncio.TimeoutError:
                        print(f"TIMEOUT la compilare pentru {child}")
                        C.kill()
                        await C.wait()
                    await asyncio.sleep(0)
                    continue

                    # stdout,_ =await C.communicate()
                    # if stdout:
                    #     print(stdout)
                    # await C.wait()

            except BadZipFile:
                continue
            except Exception as e:
                print(f"alta exceprie de la decomprimare zips: {e}")




if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description="Run a server that receives from clients zips, compiles their content, and send the binaries back, or executables"
    )
    parser.add_argument(
        "-port", "--port", metavar="port",
        required=False, help="If you want you can give a desired port for the server, default is 8008"
    )
    args = parser.parse_args()
    if args.port is not None:
        server = Server(args.port)
    else:
        server = Server()
    # print(args.port)on: ({server.server_host}, {server.server_port})")
