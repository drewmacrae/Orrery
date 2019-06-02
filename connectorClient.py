import socket
from planet import Planet
import pickle

class Network:
    def __init__(self,IP,portNo):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = IP
        self.port = portNo
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
        

    def sendstr(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)

    
    def talk(self,index,string):
        try:
            self.client.send(pickle.dumps(["talk",index,string]))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)

    def listen(self,index):
        try:
            self.client.send(pickle.dumps(["listen",index]))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)
