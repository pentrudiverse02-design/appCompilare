import json
import os.path
import socket
import asyncio
import struct
import sys

import Package
from compilType import CompilationType
from sysArhitecture import SystemArchitecture


class Client:
    listaZip = []
    serverCon = "127.0.0.1", 8008
    writer, reader = asyncio.StreamWriter, asyncio.StreamReader
    folderLocation = ""
    selectedZips = {}  # aici am facut din simplu vector in dictionar,
    # sa stiu exact cat trebuie sa primesc de la fiecare .zip in parte
    # in interiorul clientului o sa folosesc locatia completa pentru .zips
    # aceasta o sa trebuiasca sa fie stearsa pentru transmiterea ok la server
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    compileFor = CompilationType.RELEASE
    sysArhi = SystemArchitecture.x86_64
    stayInServer = False
    numeClient = ""

    def __init__(self,
                 compileType: CompilationType,
                 systemArchi: SystemArchitecture,
                 stay: bool,
                 folder: str,
                 Zips,  # aici trebuie sa fie de tip [string, string, etc]
                 nume: str):
        self.compileFor = compileType
        self.sysArhi = systemArchi
        self.stayInServer = stay
        self.folderLocation = folder
        self.ConstructZipDict(Zips)
        self.numeClient = nume

    def GetClientData(self):
        v = self.selectedZips
        v = {k.split('/')[-1]: val for k, val in self.selectedZips.items()}
        dataJson = {"name": str(self.numeClient),
                    "compileFor": str(self.compileFor),
                    "sysArhi": str(self.sysArhi),
                    "stay": self.stayInServer,
                    "expected": v,
                    "folderloc": str(self.folderLocation)}
        return json.dumps(dataJson).encode('utf-8')

    async def ConnectToServer(self):
        self.reader, self.writer = await asyncio.open_connection("127.0.0.1", 8008)
        print(f'Send: ')
        await Package.WritePackage(self.writer, Package.PackageType.LOGIN_CREDENTIALS, self.GetClientData())
        type, data = await Package.ReadPackage(self.reader)
        if type == Package.PackageType.STATUS and data.decode('utf-8') == "ok":
            print("CONECTAT CU SERVER-ul")
            await asyncio.gather(
                # self.SendAFile(),
                self.Disconect()
            )
        else:
            print("serverul nu ne da voie sa ne conectam la el.")

    def ConstructZipDict(self, Zips):
        for i in Zips:
            self.selectedZips[i] = os.path.getsize(i)

    async def SendAFile(self):
        loop = asyncio.get_event_loop()

        if self.writer is None:
            print("nu avem stream pe care sa scriem")
            return
        for i in self.selectedZips.keys():
            bufsize = self.selectedZips[i]
            with open(i, 'rb') as f:
                payload = f.read(bufsize)
                if payload is None:
                    print("payload none")
                    break
                header = struct.pack(Package.HEADER_FORMAT, int(Package.PackageType.UPLOAD_ZIP), len(payload))
                self.writer.write(header + payload)
                await self.writer.drain()
                print("am trimis zip ul")

                # await Package.WritePackage(self.writer, Package.PackageType.UPLOAD_ZIP, payload)

    async def Disconect(self):
        pass


async def main():
    a = Client(CompilationType.DEBUG, SystemArchitecture.x86_64, False, 'client_1_Folder', ["clientsFolder/p1C.zip"],
               "client1")
    await a.ConnectToServer()
    await a.SendAFile()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nClient closed.")