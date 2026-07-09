import json
import os.path
import asyncio
import struct
from Package import *
from PackageType import *

from compilType import CompilationType
from sysArhitecture import SystemArchitecture
from zips import ZipClass


class Client:
    serverCon = "127.0.0.1", 8008
    writer, reader = asyncio.StreamWriter, asyncio.StreamReader
    zipsList = []
    zipsDict = {}  # aici am facut din simplu vector in dictionar,
    # sa stiu exact cat trebuie sa primesc de la fiecare .zip in parte
    # in interiorul clientului o sa folosesc locatia completa pentru .zips
    # aceasta o sa trebuiasca sa fie stearsa pentru transmiterea ok la server
    compileFor = CompilationType.RELEASE
    sysArhi = SystemArchitecture.x86_64
    stayInServer = False

    def __init__(self,
                 compileType: CompilationType,
                 systemArchi: SystemArchitecture,
                 stay: bool,
                 folder: str,
                 Zips  # aici trebuie sa fie de tip [string, string, etc]
                 ):
        self.compileFor = compileType
        self.sysArhi = systemArchi
        self.stayInServer = stay
        self.folderLocation = folder
        self.ConstructZipDict(Zips)
        self.ZIP = None

    def GetClientData(self):
        v = self.zipsList
        self.zipsDict = {k.split('/')[-1]: val for k, val in self.zipsList}
        dataJson = {"compileFor": int(self.compileFor),
                    "sysArhi": int(self.sysArhi),
                    "stay": self.stayInServer}
        return json.dumps(dataJson).encode('utf-8')

    async def ConnectToServer(self):
        self.reader, self.writer = await asyncio.open_connection("127.0.0.1", 8008)
        print(f'Send: ')
        await WritePackage(self.writer, PackageType.LOGIN_CREDENTIALS, self.GetClientData())
        self.ZIP = ZipClass(self.writer, self.reader, "clientsFolder")
        # selectedZips trebuie sa fie construit
        self.ZIP.ZipsToSend(self.zipsDict)
        await self.ReceiveStreamHandle()

    async def ReceiveStreamHandle(self):
        while True:
            header, lenght = await ReadPackagetType(self.reader)

            match header:
                case PackageType.STATUS:
                    payload = await GetPackageContent(self.reader, lenght)
                    print(f"{payload.decode('utf-8')}")
                case PackageType.SELECTED_ZIPS:
                    payload = await GetPackageContent(self.reader, lenght)
                    self.ZIP.ZipToReceive(json.loads(payload.decode('utf-8')))
                case PackageType.ZIP:
                    self.ZIP.GetZip()
                case PackageType.DISCONNECT:
                    pass

    def ConstructZipDict(self, Zips):
        for i in Zips:
            self.zipsDict[i] = os.path.getsize(i)

    async def Disconect(self):
        pass


async def main():
    a = Client(CompilationType.DEBUG,
               SystemArchitecture.x86_64,
               False,
               'client_1_Folder',
               ["clientsFolder/p1C.zip"]
               )
    await a.ConnectToServer()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nClient closed.")
