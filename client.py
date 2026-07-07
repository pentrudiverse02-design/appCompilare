import json
import os.path
import socket
import asyncio

import Package
from compilType import CompilationType
from sysArhitecture import SystemArchitecture

class Client:
    listaZip = []
    serverCon = "127.0.0.1", 8008
    writer, reader = asyncio.StreamWriter, asyncio.StreamReader
    folderLocation = ""
    selectedZips = {} # aici am facut din simplu vector in dictionar,
                      # sa stiu exact cat trebuie sa primesc de la fiecare .zip in parte
                    #in interiorul clientului o sa folosesc locatia completa pentru .zips
                    #aceasta o sa trebuiasca sa fie stearsa pentru transmiterea ok la server
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
                 Zips, #aici trebuie sa fie de tip [string, string, etc]
                 nume: str):
        self.compileFor = compileType
        self.sysArhi = systemArchi
        self.stayInServer = stay
        self.folderLocation = folder
        self.ConstructZipDict(Zips)
        self.numeClient = nume

    def GetClientData(self):
        dataJson = {"name": str(self.numeClient),
                    "compileFor": str(self.compileFor),
                    "sysArhi": str(self.sysArhi),
                    "stay": str(self.stayInServer),
                    "expected": self.selectedZips,
                    "folderloc": str(self.folderLocation)}
        return json.dumps(dataJson).encode('utf-8')

    async def ConnectToServer(self):
        try:
            async with asyncio.timeout(1000000):
                self.reader, self.writer = await asyncio.open_connection("127.0.0.1", 8008)
                print(f'Send: ')
                await Package.WritePackage(self.writer, Package.PackageType.LOGIN_CREDENTIALS, self.GetClientData())

                type, data = await Package.ReadPackage(self.reader)
                if type == Package.PackageType.STATUS and data.decode('utf-8') == "ok":
                    print("CONECTAT CU SERVER-ul")
                else:
                    print("serverul nu ne da voie sa ne conectam la el.")
        except TimeoutError:
            print("nu se poate realiza conexiunea cu server ul")

    def ConstructZipDict(self,Zips):
        for i in Zips:
            self.selectedZips[i]=os.path.getsize(i)

    async def SendAFile(self):
        try:
            async with asyncio.timeout(1000000):
                if self.writer is None:
                    print("nu avem stream pe care sa scriem")
                    return
                for i in self.selectedZips.keys():
                    bufsize = self.selectedZips[i]
                    with open(i, 'rb') as f:
                        payload = f.read(bufsize)
                        if payload is None:
                            break
                        await Package.WritePackage(self.writer, Package.PackageType.UPLOAD_ZIP, payload)
        except:
            print("timeout din sendfile")


a = Client(CompilationType.DEBUG, SystemArchitecture.x86_64, False, 'client_1_Folder', ["clientsFolder/p1C.zip"], "client1")
asyncio.run(a.ConnectToServer())
asyncio.run(a.SendAFile())