import asyncio
import json
import os.path
from pathlib import Path
from comune.TransportSerializer import *
from comune.PacketType import *
from comune.compilType import CompilationType, CompilationTypeConvStr
from comune.sysArchitecture import SystemArchitecture, SystemArchitectureConvStr
from comune.zips import ZipClass


class Client:
    tasks = set()
    #aici trebuie sa stam pe 0.0.0.0 Pe local se asculta doar in container
    serverConAddress = "127.0.0.1"
    serverConPort = 8008
    writer, reader = asyncio.StreamWriter, asyncio.StreamReader
    compileFor = CompilationType.RELEASE
    sysArchi = SystemArchitecture.x86_64
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
                 # am scos zipList de aici, NU o sa mai fie transmis ca parametru, o sa
                 # se citeasca automat .zip din folderul clientului.
                 #
                 # acest folder o sa se contruieasca din client-run.sh
                 # in locatia clientdir/clients/NUME_FOLDER_GENERAT
                 # si o sa l populeze cu .zip din folderul ZipsToBorrow
                 # 
                 # zipsList  # aici trebuie sa fie de tip [string, string, etc]
                 # 
                 ):
        self.compileFor = compileType
        self.sysArchi = systemArchi
        self.stayInServer = stay
        self.folderLocation = "clientdir/clients/" + folder
        self.ConstructZipList()
        # self.zipsList
        # self.ConstructZipDict()
        self.ZIP = None


    def GetClientData(self):
        dataJson = {"compileFor": int(self.compileFor),
                    "sysArchi": int(self.sysArchi),
                    "stay": self.stayInServer,
                    "folder": self.folderLocation.split('/')[-1]}
        return json.dumps(dataJson).encode('utf-8')


    async def ConnectToServer(self):
        self.reader, self.writer = await asyncio.open_connection(self.serverConAddress,self.serverConPort)
        print(f'Send: ')
        await WritePacket(self.writer, PacketType.LOGIN_CREDENTIALS, self.GetClientData())
        self.ZIP = ZipClass(self.writer, self.reader, "clients")
        print(f"zips")
        self.ZIP.ZipsToSend(self.zipsDict)


    async def ReceiveStreamHandle(self):
        while True:
            if self.reader.at_eof():
                print("sunt la client, conectiune inchisa")
                exit()
            header, lenght = await ReadPacketTypeAndLength(self.reader)
            match header:
                case PacketType.STATUS:
                    payload = await GetPacketContent(self.reader, lenght)
                    print(f"{payload.decode('utf-8')}")

                case PacketType.SELECTED_ZIPS:
                    payload = await GetPacketContent(self.reader, lenght)
                    self.ZIP.ZipToReceive(json.loads(payload.decode('utf-8')))

                case PacketType.ZIP:
                    self.ZIP.GetZip()

                case PacketType.DISCONNECT:
                    pass


    async def SendZips(self):
        await self.ZIP.SendZip()


    def ConstructZipList(self):
        print()
        print("construieste zipdict din client")
        sources =  Path(self.folderLocation)
        print(sources)
        files = sources.iterdir()
        for i in files:
            self.zipsList = str(i.name)
            self.zipsDict[str(i)] = os.path.getsize(i)
        print()


    async def Disconect(self):
        print("clientul incepe deconectarea")
        if self.writer.is_closing():
            await WritePacket(self.writer, PacketType.DISCONNECT, None)
            self.writer.close()
            await self.writer.wait_closed()
        self.writer = None
        self.reader = None
        print("clientul s a deconectat")
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


    async def Ruleaza(self):
        print("conectare la server")
        await self.ConnectToServer()
        print("trimitere zips")
        await self.SendZips()
        print("deconectare")
        await self.Disconect()


def ConvertToBool( str ):
    if str =="1":
        return True
    else:
        return False

if __name__ == "__main__":
    import argparse

    parse = argparse.ArgumentParser(
        description="this is a Client app that can send .zip files to be compiled on a server "
                    "and receive the binaries, executables, or just the output"
    )
    parse.add_argument(
        "-comp", "--compileFor", metavar="compileType", type=CompilationTypeConvStr,
        required=True, choices=[CompilationType.RELEASE,CompilationType.DEBUG,CompilationType.LIBRARY],
        help="this passes the compilation type for the files. DO NOT PASS A main() function FOR LIBRARY"
    )
    # archi!!!
    parse.add_argument(
        "-archi", "--architecture", metavar="systemArchitecture", type=SystemArchitectureConvStr,
        required=True, choices=[SystemArchitecture.x86_64,SystemArchitecture.arm64,SystemArchitecture.aarch_64],
        help="this passes the target's computer architecture, Default is x86_64"
    )
    parse.add_argument(
        "-s", "--stay", metavar="stay in server",
        required=True, choices=[False, True], type=ConvertToBool,
        help="this parameter tells the server if you wish the compiled files to stay in server or not"
    )
    parse.add_argument(
        "-f", "--folder", metavar="folder", required=True,
        help="how do you wish to clients folder to be named"
    )
    args = parse.parse_args()
    print()
    print()
    print(args.compileFor)
    client = Client(args.compileFor, args.architecture, args.stay, args.folder)
    asyncio.run(client.Ruleaza())

