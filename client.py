import json
import socket
import asyncio

import Package
from compilType import CompilationType
from sysArhitecture import SystemArchitecture


class Client:
    listaZip = []
    serverCon = "127.0.0.1", 8008
    writer, reader = None, None
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
        dataJson={"name" : str(self.numeClient),
                  "compileFor" : str(self.compileFor) ,
                  "sysArhi" : str(self.sysArhi) ,
                  "stay" : str(self.stayInServer) ,
                  "folderloc" : str(self.folderLocation)}
        return json.dumps(dataJson).encode('utf-8')

    async def ConnectToServer(self):
        try:
            async with asyncio.timeout(1000):
                self.reader, self.writer = await asyncio.open_connection("127.0.0.1", 8008)
                print(f'Send: ')
                await Package.WritePackage(self.writer,Package.PackageType.LOGIN_CREDENTIALS,self.GetClientData())

                type, data = await Package.ReadPackage(self.reader)
                if type == Package.PackageType.STATUS and data.decode('utf-8')=="ok":
                    print("CONECTAT CU SERVER-ul")
                else:
                    print("serverul nu ne da voie sa ne conectam la el.")
        except TimeoutError:
            print("nu se poate realiza conexiunea cu server ul")



a=Client(CompilationType.DEBUG,SystemArchitecture.x86_64,True,'',"client3")
asyncio.run(a.ConnectToServer())