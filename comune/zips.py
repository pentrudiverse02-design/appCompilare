import json
from asyncio import *
from comune.Package import *


class ZipClass:
    def __init__(self,
                 w: StreamWriter,
                 r: StreamReader,
                 recv: str
                    # o sa trebuiasca sa facem o contrusctie de adrese
                    # o sa trebuiasca sa trimit adresa curata catre client
                    # si noi o sa trebuiasca sa citim complet fisierele
                 ):
        self.zipsToReadAndSend = {} #aici au calea completa de citire din sursa, receptorul nu trebui sa stie
        self.zipsToSend = None # aici ai doar numele zipului, nu si calea lui
        self.zipsToReceive = None
        self.reader = r
        self.writer = w
        self.ReceiverFolder = recv


    async def SendZip(self):
        if self.zipsToReadAndSend is None or self.zipsToSend is None:
            print("trebuie sa fie selectate niste .zip, err din zips.py")
            exit("zips_ERR")

        zips_safe = {str(key): value for key, value in self.zipsToSend.items()}
        #z = json.dumps(self.zipsToSend).encode('utf-8')
        z = json.dumps(zips_safe).encode('utf-8')

        await WritePackage(self.writer, PackageType.SELECTED_ZIPS, z)
        for i in self.zipsToReadAndSend.keys():
            bufsize = self.zipsToReadAndSend[i]
            with open(i, 'rb') as f:
                payload = f.read(bufsize)
                if payload is None:
                    print("payload none")
                    break
                await WritePackage(self.writer, PackageType.ZIP, payload)


    async def GetZip(self):
        if self.zipsToReceive is None:
            print("nu stim ce .zip uri sa citim, din zips.py a pocnit")
            exit('zipsErr')
        for i in self.zipsToReceive.keys():
            s = self.ReceiverFolder + '/' + i
            file = open(s, 'wb')
            payload = await self.reader.readexactly(self.zipsToReceive[i])
            # await payload.drain()
            file.write(payload)
            print("am primit un zip")


    def ZipsToSend(self, zips: dict):
        # zips = {"zip1.zip" : int(dim1), etc} and self.zipsToReadAndSend=zips.copy
        # aici e o metoda cred ca mi face de tipul POsixPath
        # self.zipsToSend = zips.copy()
        self.zipsToSend = zips.copy()
        print(f"zips to send {self.zipsToSend}")
        print(f"zips to send {self.ReceiverFolder + '/'}")
        for i in self.zipsToSend.keys():
            print(i)
            # ceva=self.ReceiverFolder + '/'+ i
            # self.zipsToReadAndSend[ceva] = self.zipsToSend[i]


    def ZipsToReceive(self, zips):
        # zips = {"zip1.zip" : int(dim1), etc} and self.zipsToSend=zips.copy
        self.zipsToReceive = json.loads(zips)