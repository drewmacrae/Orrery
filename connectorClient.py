import socket
from planet import Planet
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.0.110"
        self.port = 5555
        self.adr = (self.server, self.port)
        self.planets = self.connect()

    def getId(self):
        return self.id

    def isConnected(self):
        return self.connected

    def getPlanets(self):
        return self.planets
        
    def connect(self):
        try:
            self.client.connect(self.adr)
            self.connected = True
            data =self.client.recv(20048)
        except:
            self.connected = False
            print("Exception in connection: ")
            return None
        return pickle.loads(data)
        

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)
                  
