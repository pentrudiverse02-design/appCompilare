import json
import os.path
import asyncio
import struct
from asyncio import all_tasks
from concurrent.futures import ThreadPoolExecutor
from wsgiref.types import InputStream

from Package import *
from PackageType import *

from compilType import CompilationType
from sysArhitecture import SystemArchitecture
from zips import ZipClass


class Client:
    tasks = set()
    serverCon = "127.0.0.1", 8008
    writer, reader = asyncio.StreamWriter, asyncio.StreamReader
    compileFor = CompilationType.RELEASE
    sysArhi = SystemArchitecture.x86_64
    stayInServer = False
    zipsList = []
    zipsDict = {}  # aici am facut din simplu vector in dictionar,

    # sa stiu exact cat trebuie sa primesc de la fiecare .zip in parte
    # in interiorul clientului o sa folosesc locatia completa pentru .zips
    #   acest lucru se va face construind complet in momentul respectiv cu self.folderLocation

    def __init__(self,
                 compileType: CompilationType,
                 systemArchi: SystemArchitecture,
                 stay: bool,
                 folder: str,
                 zipsList  # aici trebuie sa fie de tip [string, string, etc]
                 ):
        self.compileFor = compileType
        self.sysArhi = systemArchi
        self.stayInServer = stay
        self.folderLocation = folder
        self.zipsList = zipsList
        self.ConstructZipDict()
        self.ZIP = None

    def GetClientData(self):
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

    async def ReceiveStreamHandle(self):
        while True:
            if self.reader.at_eof():
                print("sunt la client, conectiune inchisa")
                exit()
            header, lenght = await ReadPackagetTypeAndLength(self.reader)
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

    async def SendZips(self):
        await self.ZIP.SendZip()

    def ConstructZipDict(self):
        for i in self.zipsList:
            sizee = os.path.getsize('clientsFolder/' + i)
            self.zipsDict[str(i)] = sizee

    async def Disconect(self):
        pass

    async def InputStreamHandle(self, tg):
        while True:
            # 1. SCHIMBARE CRITICĂ: to_thread lasă bucla asincronă să ruleze în fundal
            meniu = ("introduceti ce doriti: \n"
                     "1 conectare la server:\n"
                     "2 trimitere fisiere\n"
                     "3 deconectare\n -> ")

            text_primit = await asyncio.to_thread(input, meniu)

            # 2. Validăm inputul ca să nu crape programul dacă introduci o literă din greșeală
            try:
                inp = int(text_primit.strip())
            except ValueError:
                print("\nTe rugăm să introduci un număr valid (1, 2 sau 3).\n")
                continue

            match inp:
                case 1:
                    tg.create_task(self.ConnectToServer())
                    await asyncio.sleep(0)
                case 2:
                    tg.create_task(self.SendZips())
                    await asyncio.sleep(0)
                case 3:
                    await self.Disconect()
                    break
                case _:
                    print("\n\na fost introdus ceva ce nu ne asteaptam in InputStreamHandle\n")


async def main():
    a = Client(CompilationType.DEBUG,
               SystemArchitecture.x86_64,
               False,
               'client_1_Folder',
               ["p1C.zip"]
               )

    async with asyncio.TaskGroup() as tg:
        await a.InputStreamHandle(tg)
    # await a.ConnectToServer()
    # await a.SendZips()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nClient closed.")