import pygame
import random
import string
import math
from connectorClient import Network
import pickle
from planet import Planet
from vectormath import *
import sys

pygame.init()
screenSize = (1280,800)
win = pygame.display.set_mode(screenSize)
pygame.display.set_caption("Connector")

yscaling = 0.3
zscaling = math.sqrt(3)/3

screenCenter = (screenSize[0]/2,screenSize[1]/2)

width = 2
height = 2

clock = pygame.time.Clock()

messages = ""

songIndex = 0
songList = ['3. Mercury.ogg','1. Mars.ogg','2. Venus.ogg','4. Jupiter.ogg','6. Uranus.ogg']

def nextSong():
    global songIndex
    #currently unused
    #start next new song (can't be current one.)
    songIndex=(songIndex+random.randint(1,len(songList)-1))%len(songList)
    pygame.mixer.music.load(songList[songIndex])
    pygame.mixer.music.play()

class FPSDisplay:
    #display FPS in upper left. I thought it was slow and wanted to check to see if it really was
    #pygame.font.init()
    #myfont = pygame.font.SysFont('Courier MS', 14)
    def displayFPS(self):
        #textsurface = self.myfont.render(str(clock.get_fps())[:5], True, (255, 255, 255))
        #win.blit(textsurface,(0,0))
        pass
class MessageBox:
    messageBoxFontSize = 18
    messageBoxspacing = 18
    #display messageBox in the upper right
    pygame.font.init()
    myfont = pygame.font.Font('OpenSans-Regular.ttf', messageBoxFontSize)
    def displayMessages(self):
        global messages
        textsurface = self.myfont.render(talkstring, True,(255,255,255))
        win.blit(textsurface,(screenSize[0]-258,0))
        
        messageList = messages.split("\n")
        if(len(messageList)>20):
            messageList = messageList[-20:]#take only the end of the messageList
        if(len(messages)>4000):
            messages = messages[-4000:]
        offset = 0#FIXME right should work but I'm getting an empty thing from the listself.messageBoxspacing;
        for eachMessage in messageList[::-1]:
            textsurface = self.myfont.render(eachMessage, True,(255,255,255))
            win.blit(textsurface,(screenSize[0]-258,offset))
            offset += self.messageBoxspacing

depletionRate = 0.005
        
class player:
    position = [500.0,500.0,0.0]
    resources = [255.0,255.0,255.0]
    target = None
    at = None
    velocity = 0.05
    def talk(self,string):
        global messages
        if self.at!=None:
            if n and n.isConnected():
                response = n.talk(self.at.index,string)
            else:
                response = self.at.talk(string)
            print(response)
            messages+=">"+response+"\n"
                
    def step(self):
        global messages
        assert(tickTime>0)
        
        if self.resources[1]>1:
            self.resources[1]-=tickTime*depletionRate/2
            assert(self.resources[1]<255)
        else:
            self.resources[0]-=tickTime*depletionRate
            
        if self.target!=None:
            if self.at!=None:
                #departing
                self.at = None
                if n and n.isConnected():
                    n.depart()
                #print("Departing")
                #Thank you to Soughtaftersounds at freesound for the music box
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('145434_2615119-lq.ogg'))
                "Copyright © 2011 Varazuvi™ www.varazuvi.com"
            if self.resources[2]>1:
                self.resources[2]-=tickTime*depletionRate
            else:
                self.resources[0]-=tickTime*depletionRate
            self.velocity = self.resources[2]/255*0.08

            #AUTOMATIC TRAVEL
            Vector2Target = sub(self.target.position,self.position)
            self.position = add(self.position,scale(self.velocity*tickTime,normalize(Vector2Target)))
            if magnitude(Vector2Target)<self.target.size:
                self.at = self.target
                self.target=None
                #arriving
                if n and n.isConnected():
                    n.arrive(self.at.index)
                #Thank you to Soughtaftersounds at freesound for the menu sparkle
                #https://freesound.org/people/Soughtaftersounds/sounds/145459/
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('145459_2615119-lq.ogg'))

        if self.at != None:
            #We're at a planet, listen to what it has to say
            if random.randint(0,10000)<tickTime:
                if n and n.isConnected():
                    response = n.listen(self.at.index)
                else:
                    response = self.at.listen()
                print(response)
                messages+=response+"\n"
                #Thank you to jotliner at freesound for the quindar tone!
                pygame.mixer.Channel(0).play(pygame.mixer.Sound('200813_2585050-lq.ogg'))

                

            #We're at a planet, take resources
            if(self.resources[0]<self.at.resources[0]):
                self.resources[0]+=0.1*tickTime
                
                #red depletes faster
                self.at.resources[0]-=0.1*tickTime/self.at.size**2
                if self.resources[0]>self.at.resources[0]:
                    self.resources[0]=self.at.resources[0]
            if(self.resources[1]<self.at.resources[1]):
                self.resources[1]+=0.1*tickTime
                if self.resources[1]>self.at.resources[1]:
                    self.resources[1]=self.at.resources[1]
                    self.at.resources[1]-=0.01*tickTime/self.at.size**2
                else:
                    self.at.resources[1]-=0.1*tickTime/self.at.size**2
            if(self.resources[2]<self.at.resources[2]):
                self.resources[2]+=0.1*tickTime
                if self.resources[2]>self.at.resources[2]:
                    self.resources[2]=self.at.resources[2]
                    self.at.resources[2]-=0.01*tickTime/self.at.size**2
                else:
                    self.at.resources[2]-=0.1*tickTime/self.at.size**2

            #print(self.at.resources)
        if(self.resources[0]<1):
            pygame.quit()
    def draw(self):
        pygame.draw.rect(win,(255,10,10),(0,screenSize[1]-30,258,10))
        pygame.draw.rect(win,(10,255,10),(0,screenSize[1]-20,258,10))
        pygame.draw.rect(win,(10,10,255),(0,screenSize[1]-10,258,10))
        pygame.draw.rect(win,(10,10,10),(256,screenSize[1]-29,-254+self.resources[0],8))
        pygame.draw.rect(win,(10,10,10),(256,screenSize[1]-19,-254+self.resources[1],8))
        pygame.draw.rect(win,(10,10,10),(256,screenSize[1]-9,-254+self.resources[2],8))



        
run = True
fps = FPSDisplay()
msgs = MessageBox()

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


#before drawing anything we'll try to connect
if len(sys.argv)==3:
    n = Network(sys.argv[1],int(sys.argv[2]))
    #I haven't gotten online multiplayer working, just ran out of time
    #n = Network("lit-dawn-45776.herokuapp.com",80)
else:
    print("could not connect to server, running a local game")
    print("first run connectorServer.py with the server IP and ports as args: eg ")
    print("py connectorServer.py 192.168.0.110 5555")
    print("For local multiplayer start use server IP and port as args: eg.") 
    if(sys.argv[0][-4:]==".exe"):
        print(sys.argv[0]," 192.168.0.110 5555")
    else:
        print("py ",sys.argv[0]," 192.168.0.110 5555")

    n = None
    
#and load the planets
if n and n.isConnected() and n.getPlanets() != None:
    planets = n.getPlanets()
    earth = planets[0]

myPlayer = player()
myPlayer.target = earth

#pygame.mixer.music.load('145434_2615119-lq.ogg')
#pygame.mixer.music.load('3. Mercury.ogg')
#for eachSong in songList[1:]:
#    pygame.mixer.music.queue(eachSong)
#    songIndex=(songIndex+1)%len(songList)
#pygame.mixer.music.play()
          
talkstring = ">"

while run:
    if not pygame.mixer.music.get_busy():
        nextSong()
    
    win.fill((0,0,0))
    #timing
    tickTime = clock.tick()
    fps.displayFPS()
    msgs.displayMessages()

    #CONTROLLER
    for event in pygame.event.get():
        #list of events show up here
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            #if you click on a planet fly to it
            mousePos = pygame.mouse.get_pos()
            clicked_sprites = [s for s in planets if s.collidepoint(mousePos)]
            if len(clicked_sprites):
                myPlayer.target = clicked_sprites[0]
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                if myPlayer.at != None:
                    myPlayer.talk(talkstring[1:])
                    talkstring = ">"
            if len(pygame.key.name(event.key))==1:
                talkstring+=pygame.key.name(event.key)
                    

    #keyboard controller that monitors currently down keys uses this:
    keys = pygame.key.get_pressed()

    #MODEL
    myPlayer.step()
    
    #VIEW
    #draw planets
    for eachPlanet in planets:
        eachPlanet.draw(win,screenCenter,yscaling,zscaling)
    #draw player
    pos = (int(screenCenter[0]+myPlayer.position[0]),int(screenCenter[1]+yscaling*myPlayer.position[1]+zscaling*myPlayer.position[2]))
    proj = (int(screenCenter[0]+myPlayer.position[0]),int(screenCenter[1]+yscaling*myPlayer.position[1]))
    pygame.draw.line(win,(32,32,32),pos,proj)
    pygame.draw.rect(win,(myPlayer.resources[0],myPlayer.resources[1],myPlayer.resources[2]),(pos[0],pos[1],width,height))
    myPlayer.draw()

    pygame.display.update()

pygame.quit()
