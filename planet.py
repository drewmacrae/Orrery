import random
import pygame
from vectormath import *
from onlineMarkov import OnlineMarkov
import pygame.gfxdraw
import math
import numpy as np

NUMBEROFPLANETS = 15

def getY(srcobject):
    return srcobject.position[1]

def aafilledcircle(win,pos,size,color):
    pygame.gfxdraw.aacircle(win,int(pos[0]),int(pos[1]),int(size),color)
    pygame.gfxdraw.filled_ellipse(win,int(pos[0]),int(pos[1]),int(size),int(size),color)

suntutorial = ["welcome to orrery, a model system.",
            "welcome to orrery, a language toy.",
            "welcome to sun, a white star."
            "fly around by clicking on the planets.",
            "welcome traveller, to orrery.",
            "shorter trips are safer.",
            "don't fly too far.",
            "this system is called orrery",
            "this body is the sun",
            "planets will supply what they can.",
            "talk with the locals by typing and pressing enter.",
            "you may encounter a fellow traveller.",
            "there are other travellers.",
            "you might be lost to space.",
            "take care traveller.",
            "click on a nearby planet."
            "planets give you resources.",
            "don't run out of resources.",
            "planets have resources.",
            "go to the planets for resources.",
            "visit the planets!",
            "talk to fellow travellers.",
            "find other travellers.",
            "to fly to a planet click on it."]

class Planet:
    def __init__(self, control = "RANDOM"):
        if(control=="SUN"):
            self.initsun()
            return
        self.index = random.randint(0,2147483647)#I want these to be indicies but here I can assure they're unique which is a start
        self.resources = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
        self.size = random.lognormvariate(1.5,0.6)
        self.culture = OnlineMarkov()
        for i in range(-1,int(self.size*2/2)):
            cultureString = self.culture.randomString(int(self.size*2/2))
            #print(cultureString)
            self.culture.contribute(cultureString)
        #old style position generation
        #self.position = [random.normalvariate(0,200),random.normalvariate(0,200),random.normalvariate(0,75)]
        #self.radius = magnitude(self.position)
        self.radius = random.lognormvariate(math.log(500),0.5)
        #print(self.radius)
        self.inclination = random.normalvariate(0,15)
        self.longitudeAscendingNode = random.uniform(0,360)
        self.trueAnomaly = random.uniform(0,360)
        self.period = math.sqrt(self.radius**3)*25
        self.rotationMatrix = Planet.eulerAngles2Matrix(self.inclination,self.longitudeAscendingNode)
        self.position = self.getPosition()

    def eulerAngles2Matrix(x,z):
        thetaZ = z*math.pi/180.0
        Rz = [    [math.cos(thetaZ),    -math.sin(thetaZ),    0],
                [math.sin(thetaZ),    math.cos(thetaZ),    0],
                [0,                    0,                    1]]
        thetaX = x*math.pi/180.0
        Rx = [    [1,    0,                    0],
                [0,    math.cos(thetaX),    -math.sin(thetaX)],
                [0,    math.sin(thetaX),    math.cos(thetaX)]]
        return np.matmul(Rz,Rx)

    def initsun(self):
        self.size = 40
        self.radius = 0
        self.position = [0.0,0.0,0.0]
        self.resources = [225.0,225.0,225.0]
        self.culture = OnlineMarkov()
        self.culture.erase()#clear out the dictionary on sun for a suntutorial
        for tutorialLine in suntutorial:
            self.culture.contribute(tutorialLine)
            #the suntutorial dictionary is committed twice to help it to speak more cogently.
            self.culture.contribute(tutorialLine)
        #self.culture.print()
        self.trueAnomaly = 0
        self.period = 22
        self.rotationMatrix = [[1,0,0],[0,1,0],[0,0,1]]


    def getPosition(self):
        #compute position in the plane of the orbit
        x = self.radius*math.sin(self.trueAnomaly*math.pi/180.0)
        y = self.radius*math.cos(self.trueAnomaly*math.pi/180.0)
        z = 0

        #ignore inclination and longitude of ascending node for now
        return add(np.matmul(self.rotationMatrix,[x,y,z]),[0,0,200])

    def step(self,tick):
        #position update
        self.trueAnomaly += 360.0*tick/self.period
        if self.trueAnomaly>=360:
            self.trueAnomaly-=360
        self.position = self.getPosition()

        #resource update
        #if self.resources[1]<1:
        #    if self.resources[0]>1:
        #        self.resources[0] -= 


    def generatePlanetList():
        #initialize sun, the tutorial planet
        sun = Planet("SUN")
        planetList = [sun]

        #set sun as resting on the "table"
        minZ = 10

        for i in range(NUMBEROFPLANETS):
            planetList = planetList+[Planet()]
        for eachPlanet in planetList:
            if(eachPlanet.position[2]<minZ):
                minZ = eachPlanet.position[2]
        for eachPlanet in planetList:
            eachPlanet.position[2] -= minZ-eachPlanet.size

        #planetList.sort(key = getY)
        return [sun,planetList]

    def drawReflections(self,win,screenCenter,yscaling,zscaling):
        if(self.position[2]>0):
            dimColor = (self.resources[0]*0.25,self.resources[1]*0.25,self.resources[2]*0.25)
            proj = (screenCenter[0]+self.position[0],screenCenter[1]+yscaling*self.position[1])
            self.npos =  (screenCenter[0]+self.position[0],screenCenter[1]+yscaling*self.position[1]-zscaling*self.position[2])
            pygame.draw.aaline(win,(16,16,16),self.npos,proj)
            aafilledcircle(win,self.npos,self.size,dimColor)

    def drawImages(self,win,screenCenter,yscaling,zscaling):
        planetColor = (self.resources[0],self.resources[1],self.resources[2])
        self.pos = (screenCenter[0]+self.position[0],screenCenter[1]+yscaling*self.position[1]+zscaling*self.position[2])
        proj = (screenCenter[0]+self.position[0],screenCenter[1]+yscaling*self.position[1])
        pygame.draw.aaline(win,(64,64,64),self.pos,proj)
        aafilledcircle(win,self.pos,self.size,planetColor)

    def collidepoint(self,mousePos):
        if(magnitude(sub(self.pos,mousePos))<self.size+5):
            #self.print()
            return True
        return False
    def print(self):
        print(self.resources)
        print(self.size)
        print(self.culture)
        print(self.position)
        
    def listen(self):
        return self.culture.generate()

    def talk(self,string):
        self.culture.contribute(string)