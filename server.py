import asyncio
from email import message


class Server:
    clients={}
    server_host = '127.0.0.1' 
    server_port = 8008
    folderServer = ''
    maxConnections = 0
    SERVER=0
    def __init__(self):
        asyncio.run(self.CreateServer())
    async def CreateServer(self):
        self.SERVER= await asyncio.start_server(self.ClientConnect,self.server_host,self.server_port)

        addrs = ', '.join(str(sock.getsockname()) for sock in self.SERVER.sockets)
        print(f'Serving on {addrs}')
        async with self.SERVER:
            await self.SERVER.serve_forever()



    async def ClientConnect(self,reader,writer):
        data = await reader.read(1024)
        message = data.decode('utf-8')
        addr = writer.get_extra_info('peername')
        print(f"am primit {message} de la {addr}")
        writer.write("ok".encode('utf-8'))
        await writer.drain()

Server()