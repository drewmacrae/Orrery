import socket
from _thread import *
import sys

#socket allows for incoming connections
server = "192.168.0.110"
port = 5555

#IPV4
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server,port))
except socket.error as e:
    print(e)

#listen for up to 10 connections
s.listen(10)
print("Waiting for connection...")

def threaded_client(conn):
    conn.send(str.encode("Welcome client to connector server"))
    reply = ""
    while True:
        try:
            #object truancy occurs if object too big to fit
            data = conn.recv(2048)
            reply = data.decode("utf-8")

            if not data:
                print("Disconnected")
                break
            else:
                print("Recv: ",reply)
                print("Sending: ",reply)

            conn.sendall(reply.encode("utf-8"))
        except:
            break
    print("Error in connection loop")
    conn.close()

while True:
    #oh right because python does pattern matching :D
    conn, adr = s.accept()
    print("Connected to:", adr)

    start_new_thread(threaded_client, (conn,))
    
