import socket
from _thread import *
import sys
from planet import Planet
import pickle

if len(sys.argv)!=3:
    print("usage: ",sys.argv[0]," 192.168.1.1 5555")
    print("use your IP address in place of 192.168.1.1 and an open port in place of 5555")
    exit()
    
#socket allows for incoming connections
#server = "192.168.0.110"
#port = 5555
server = sys.argv[1]
port = int(sys.argv[2])

#IPV4
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server,port))
except socket.error as e:
    print(e)

def getY(srcobject):
    return srcobject.position[1]

#instantiate local planets
earth = Planet()
earth.size = 10
earth.position = [0.0,0.0,0.0]
earth.resources = [32.0,192.0,128.0]
planets = [earth]

for i in range(40):
    planets = planets+[Planet()]

planets.sort(key = getY)

for i in range(41):
    planets[i].index = i


#listen for up to 10 connections
maxPlayers = 10
s.listen(maxPlayers)
print("Waiting for connection...")

playerLock = allocate_lock()
players = 0
playerSlots = [False]*maxPlayers
playersAt = [-1]*maxPlayers
messageQueues = [""]*maxPlayers#I might need a lock

def threaded_client(conn):
    global playerSlots
    global players

    #find our player number so the server can share things between threads
    playerLock.acquire()
    players+=1
    playerNumb=0
    print(playerSlots)
    while playerSlots[playerNumb]:
        playerNumb+=1
        print(playerNumb)
    print(playerNumb)
    playerSlots[playerNumb]=True
    playerLock.release()
    
    conn.send(pickle.dumps(planets))
    reply = ""
    at = None
    while True:
        try:
            #object truancy occurs if object too big to fit
            data = conn.recv(2048)
            reply = pickle.loads(data)

            if not data:
                print("Disconnected")
                break
            else:
                print("Recv: ",reply)
                if(len(reply)==1):
                    if(reply[0]=="depart"):
                        playersAt[playerNumb] = -1
                        at = None
                if(len(reply)==2):
                    if(reply[0]=="arrive"):
                        at = reply[1]
                        playersAt[playerNumb] = reply[1]
                    if(reply[0]=="listen"):
                        at = reply[1]
                        playersAt[playerNumb] = reply[1]
                        reply = planets[reply[1]].listen()
                        if(len(messageQueues[playerNumb])):
                            reply = messageQueues[playerNumb]
                            messageQueues[playerNumb] = ""
                if(len(reply)==3):
                    if(reply[0]=="talk"):
                        print(playerNumb," is talking at: ",reply[1]," saying ",reply[2])
                        print(playersAt)
                        print(playerSlots)
                        print(messageQueues)
                        for index in range(maxPlayers):
                            if index != playerNumb and reply[1] != -1 and playersAt[index] == reply[1] and playerSlots[index]:
                                print("found ",index)
                                messageQueues[index]+=reply[2]
                                print(messageQueues)
                        reply = planets[reply[1]].talk(reply[2])
                print("Sending: ",reply)

            conn.sendall(pickle.dumps(reply))
        except:
            break
    print("Error in connection loop")
    conn.close()
    playerLock.acquire()
    players -=1
    playerSlots[playerNumb] = False
    playerLock.release()
    
while True:
    #oh right because python does pattern matching :D
    conn, adr = s.accept()
    print("Connected to:", adr)

    start_new_thread(threaded_client, (conn,))
    
