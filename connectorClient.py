import socket

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.0.110"
        self.port = 5555
        self.adr = (self.server, self.port)
        self.id = self.connect()
        print(self.id)

    def getId():
        return self.id
        
    def connect(self):
        try:
            self.client.connect(self.adr)
            return self.client.recv(2048).decode()
        except:
            print("Exception in connection")

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)
                  
