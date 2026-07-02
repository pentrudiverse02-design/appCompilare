import socket
from tkinter import BooleanVar, StringVar

from compilType import CompilationType
from sysArhitecture import SystemArchitecture


class Client:
    listaZip = []
    serverCon = ("127.0.0.1", 8008)
    folderLocation = ""
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    compileFor = CompilationType.RELEASE
    sysArhi = SystemArchitecture.x86_64
    stayInServer = False
    numeClient = ""

    def __init__(self,
                 compileType: CompilationType,
                 systemArchi: SystemArchitecture,
                 stay: BooleanVar,
                 folder: StringVar,
                 nume: StringVar):
        self.compileFor = compileType
        self.sysArhi = systemArchi
        self.stayInServer = stay
        self.folderLocation = folder
        self.numeClient = nume

    def GetClientData(self):
        return "name" + str(self.numeClient) + "compileFor" + str(self.compileFor) + "sysArhi" + str(self.sysArhi)+ "stay" + str(self.stayInServer) + "folderloc" + str(self.folderLocation)

    def ConnectToServer(self):
        self.socket.connect(self.serverCon)
        self.socket.sendall(self.GetClientData().encode('utf-8'))