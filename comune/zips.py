import json
from asyncio import *
from comune.TransportSerializer import *


class ZipClass:
    def __init__(self,
                 w: StreamWriter,
                 r: StreamReader,
                 recv: str
                    #o sa trebuiasca sa facem o contrusctie de adrese
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
        z = json.dumps(self.zipsToSend).encode('utf-8')
        await WritePacket(self.writer, PacketType.SELECTED_ZIPS, z)
        for i in self.zipsToReadAndSend.keys():
            bufsize = self.zipsToReadAndSend[i]
            with open(i, 'rb') as f:
                payload = f.read(bufsize)
                if payload is None:
                    print("payload none")
                    break
                await WritePacket(self.writer, PacketType.ZIP, payload)

                # header = struct.pack(HEADER_FORMAT, int(PacketType.UPLOAD_ZIP), len(payload))
                # self.writer.write(header + payload)
                # await self.writer.drain()
                print("am trimis zip ul")
        # self.zipsToSend = None

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
            print()
            print()


    def ZipsToSend(self, zips: dict):
        # zips = {"zip1.zip" : int(dim1), etc} and self.zipsToReadAndSend=zips.copy
        self.zipsToSend = {z.split('/')[-1]: b for z, b in zips.items()}

        for i in zips.keys():
            # self.zipsToReadAndSend[str(self.ReceiverFolder) + '/'+ str(i)] = self.zipsToSend[i]
            self.zipsToReadAndSend[str(i)] = zips[i]

    def ZipsToReceive(self, zips:dict):
        # zips = {"zip1.zip" : int(dim1), etc} and self.zipsToSend=zips.copy
        # a=json.loads(zips).decode('utf-8')

        # self.zipsToReceive = zips.copy()
        # print(f"am primit zipsToReceive {self.zipsToReceive}")

        self.zipsToReceive = zips
        print(f"ce anume o sa trbeuiasca sa primesc: {type(self.zipsToReceive)} si {self.zipsToReceive}")