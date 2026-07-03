import socket
import asyncio
from compilType import CompilationType
from sysArhitecture import SystemArchitecture


class Client:
    listaZip = []
    serverCon = "127.0.0.1", 8008
    reader ,writer = 0 , 0
    folderLocation = ""
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    compileFor = CompilationType.RELEASE
    sysArhi = SystemArchitecture.x86_64
    stayInServer = False
    numeClient = ""

    def __init__(self,
                 compileType: CompilationType,
                 systemArchi: SystemArchitecture,
                 stay: int,
                 folder: str,
                 nume: str):
        self.compileFor = compileType
        self.sysArhi = systemArchi
        self.stayInServer = stay
        self.folderLocation = folder
        self.numeClient = nume

    def GetClientData(self):
        return "name" + str(self.numeClient) + "compileFor" + str(self.compileFor) + "sysArhi" + str(self.sysArhi)+ "stay" + str(self.stayInServer) + "folderloc" + str(self.folderLocation)

    async def ConnectToServer(self):
        try:
            async with asyncio.timeout(100):
                self.reader, self.writer = await asyncio.open_connection("127.0.0.1", 8008)
                print(f'Send: ')
                self.writer.write(self.GetClientData().encode())
                await self.writer.drain()

                data = await self.reader.read(100)
                if data.decode('utf-8') != "ok":
                    print("serverul nu ne da voie sa ne conectam la el.")
                else:
                    print("CONECTAT CU SERVER-ul")
        except TimeoutError:
            print("nu se poate realiza conexiunea cu server ul")

        # try:
        #     async with asyncio.timeout(10) as expCon:
        #         self.socket.connect(self.serverCon)
        # except:
        #     print("eroare la conexiune")
        # if expCon.expired():
        #     print("a expirant timpul pentru conexiunea cu serverul!")
        #     print("mai incercam conexiunea!")
        #     #reincercam conexiunea
        #     self.ConnectToServer()
        #     #reincercam conexiunea
        #
        # else:
        #     try:
        #         async with asyncio.timeout(10) as expSendData:
        #             self.socket.sendall(self.GetClientData().encode('utf-8'))
        #
        # while True:
        #     data = self.socket.recv(1024)
        #     if data:
        #         data=data.decode('utf-8')
        #         if data=="ok":
        #             return True
