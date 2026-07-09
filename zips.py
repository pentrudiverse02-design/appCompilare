import json
from asyncio import *
from Package import *


class ZipClass:
    def __init__(self,
                 w: StreamWriter,
                 r: StreamReader,
                 recv: str
                 # sen: str, # nu mai vreau nume folder trimitere,
                            # nu o sa construiesc adresele de citire
                            # o sa vina deja complete in ZipsToSend
                 ):
        self.zipsToSend = None
        self.reader = r
        self.writer = w
        self.ReceiverFolder = recv
        # self.SendFolder = sen

    async def SendZip(self):
        if self.zipsToSend == None:
            print("trebuie sa fie selectate niste .zip, err din zips.py")
            exit("zips_ERR")
        z=json.dumps(self.zipsToSend).encode('utf-8')
        asyncio.run(WritePackage(self.writer,PackageType.SELECTED_ZIPS,z))
        for i in self.zipsToSend.keys():
            bufsize = self.zipsToSend[i]
            with open(i, 'rb') as f:
                payload = f.read(bufsize)
                if payload is None:
                    print("payload none")
                    break
                await WritePackage(self.writer, PackageType.ZIP, payload)

                # header = struct.pack(HEADER_FORMAT, int(PackageType.UPLOAD_ZIP), len(payload))
                # self.writer.write(header + payload)
                # await self.writer.drain()
                print("am trimis zip ul")
        self.zipsToSend = None

    async def GetZip(self):
        if self.zipsToReceive is None:
            print("nu stim ce .zip uri sa citim, din zips.py a pocnit")
            exit('zipsErr')
        for i in self.zipsToReceive:
            s=self.ReceiverFolder+'/'+i
            file=open(s,'wb')
            payload= await self.reader.readexactly(self.zipsToReceive[i])
            #await payload.drain()
            file.write(payload)



    def ZipsToSend(self, zips: dict):
        # zips = {"zip1.zip" : int(dim1), etc} and self.zipsToSend=zips.copy
        self.zipsToSend = zips.copy()
    def ZipsToReceive(self, zips:dict):
        # zips = {"zip1.zip" : int(dim1), etc} and self.zipsToSend=zips.copy
        # a=json.loads(zips).decode('utf-8')
        self.zipsToReceive = zips
