import asyncio
from email import message


class Server:
    clients={}
    server_host = '127.0.0.1' 
    server_port = 8008
    folderServer = ''
    maxConnections = 0
    SERVER=None
    def __init__(self):
        asyncio.run(self.CreateServer())
    async def CreateServer(self):
        self.SERVER = await asyncio.start_server(self.ClientHandle,self.server_host,self.server_port)
        addrs = ', '.join(str(sock.getsockname()) for sock in self.SERVER.sockets)
        print(f'Serving on {addrs}')
        async with self.SERVER:
            await self.SERVER.serve_forever()

    async def ClientConnect(self,addr,reader:asyncio.StreamReader,writer:asyncio.StreamWriter):
        data= await reader.read(1024)
        data=data.decode('utf-8')
        self.clients[addr]={reader,writer,data}
        writer.write("ok".encode('utf-8'))
        await writer.drain()

    async def ClientHandle(self,reader:asyncio.StreamReader,writer:asyncio.StreamWriter):
        if not self.clients.__contains__(writer.get_extra_info('peername')):
            self.ClientConnect(writer.get_extra_info('peername'), reader,writer)
        data = await reader.read(1024)
        message = data.decode('utf-8')
        addr = writer.get_extra_info('peername')
        print(f"am primit {message} de la {addr}")
        self.clients[addr]=message
        writer.write("ok".encode('utf-8'))
        await writer.drain()

while True:
    a=Server()
    print("introduceti ce doriti sa faceti cu urmatoarele coenxiuni:")
    for i in a.clients:
        print(f" client {i} ", end ='' )