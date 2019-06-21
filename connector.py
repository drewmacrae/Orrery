import pygame
import random
import string
import math
from connectorClient import Network
import pickle
from planet import Planet
from vectormath import *
import sys
from messageBox import MessageBox
from messageBox import Message
from player import Player
import profile
FPSON = False
if FPSON:
	from FPSDisplay import FPSDisplay

pygame.init()
screenSize = (1280,800)
win = pygame.display.set_mode(screenSize)
pygame.display.set_caption("orrery")
screenShotAfterRender = False

reflectionimages = pygame.Surface(screenSize, pygame.SRCALPHA)
planetimages = pygame.Surface(screenSize, pygame.SRCALPHA)
shipimages = pygame.Surface(screenSize, pygame.SRCALPHA)

yscaling = 1.0/3.0
zscaling = -math.sqrt(3.0)/3.0

screenCenter = (screenSize[0]/2,screenSize[1]/2)

width = 2
height = 2

clock = pygame.time.Clock()

songIndex = 0
songList = ['3. Mercury.ogg','1. Mars.ogg','2. Venus.ogg','4. Jupiter.ogg','6. Uranus.ogg']

def nextSong():
    global songIndex
    #currently unused
    #start next new song (can't be current one.)
    songIndex=(songIndex+random.randint(1,len(songList)-1))%len(songList)
    pygame.mixer.music.load(songList[songIndex])
    pygame.mixer.music.play()
        
run = True
if FPSON: fps = FPSDisplay()
msgs = MessageBox(screenSize)

def getY(srcobject):
    return srcobject.position[1]
    
#instantiate local planets
[sun,planets] = Planet.generatePlanetList()

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
    print("\n")
    n = None
    
#and load the planets
if n and n.isConnected() and n.getPlanets() != None:
    planets = n.getPlanets()
    sun = planets[0]

myPlayer = Player(planets,msgs)
myPlayer.target = sun


while run:
    win.fill((10,10,25))
    if not pygame.mixer.music.get_busy():
        nextSong()
    
    #timing
    tickTime = clock.tick()
    if FPSON: fps.displayFPS(win,clock)
    msgs.displayMessages(win,tickTime,myPlayer.resources)

    #CONTROLLER
    for event in pygame.event.get():
        #list of events show up here
        if event.type == pygame.QUIT:
            run = False
            exit()
        if event.type == pygame.MOUSEBUTTONUP:
            #if you click on a planet fly to it
            mousePos = pygame.mouse.get_pos()
            clicked_sprites = [s for s in planets if s.collidepoint(mousePos)]
            if len(clicked_sprites):
                myPlayer.target = clicked_sprites[0]
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                if myPlayer.at != None:
                    myPlayer.talk(msgs.talkstring[1:])
                    msgs.talkstring = ">"
            if event.key == pygame.K_SPACE:
                msgs.talkstring+=" "
            if event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                if(len(msgs.talkstring)>1):
                    msgs.talkstring = msgs.talkstring[:-1]
            if event.key == pygame.K_PRINT or event.key == pygame.K_F12:
                screenShotAfterRender = True
            if len(pygame.key.name(event.key))==1:
                msgs.talkstring+=pygame.key.name(event.key)
                    

    #keyboard controller that monitors currently down keys uses this:
    keys = pygame.key.get_pressed()

    #MODEL
    myPlayer.step(tickTime)    
    for eachPlanet in planets:
    	eachPlanet.step(tickTime)

    #VIEW
    #draw planets

    sortedPlanets = planets
    sortedPlanets.sort(key = getY)
    for eachPlanet in sortedPlanets:
        eachPlanet.drawReflections(win,screenCenter,yscaling,zscaling)
    for eachPlanet in sortedPlanets:
        eachPlanet.drawImages(win,screenCenter,yscaling,zscaling)

    #draw player
    pos = (int(screenCenter[0]+myPlayer.position[0]),int(screenCenter[1]+yscaling*myPlayer.position[1]+zscaling*myPlayer.position[2]))
    proj = (int(screenCenter[0]+myPlayer.position[0]),int(screenCenter[1]+yscaling*myPlayer.position[1]))
    pygame.draw.line(win,(32,32,32),pos,proj)
    pygame.draw.rect(win,(myPlayer.resources[0],myPlayer.resources[1],myPlayer.resources[2]),(pos[0],pos[1],width,height))
    myPlayer.draw(win,screenSize)

    pygame.display.update()
    if screenShotAfterRender:
        screenShotAfterRender=False
        pygame.image.save(win,"Orrery_"+str(random.randint(1,2147483648))+".png")
        #Camera Shutter, Fast, A
        pygame.mixer.Channel(2).play(pygame.mixer.Sound('360329_5121236-lq.ogg'))

pygame.quit()
exit()
