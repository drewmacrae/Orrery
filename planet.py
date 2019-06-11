import random
import pygame
from vectormath import *
from onlineMarkov import OnlineMarkov
import pygame.gfxdraw

def getY(srcobject):
    return srcobject.position[1]

def aafilledcircle(win,pos,size,color):
    pygame.gfxdraw.aacircle(win,pos[0],pos[1],int(size),color)
    pygame.gfxdraw.filled_circle(win,pos[0],pos[1],int(size),color)

tutorial = ["welcome to orrery, a model system.",
			"welcome to orrery, a language toy.",
			"fly around by clicking on the planets.",
			"click on planets.",
			"shorter trips are safer.",
			"don't fly too far.",
			"this system is called orrery",
			"this planet is called earth",
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
    def generatePlanetList():
        earth = Planet()
        earth.size = 10
        earth.position = [0.0,0.0,0.0]
        earth.resources = [32.0,192.0,128.0]
        earth.culture.erase()#clear out the dictionary on earth for a tutorial
        for tutorialLine in tutorial:
        	earth.culture.contribute(tutorialLine)
        #earth.culture.print()
        planetList = [earth]

        minZ = 10

        for i in range(20):
            planetList = planetList+[Planet()]
        for eachPlanet in planetList:
            if(eachPlanet.position[2]<minZ):
                minZ = eachPlanet.position[2]
        for eachPlanet in planetList:
            eachPlanet.position[2] -= minZ-eachPlanet.size

        planetList.sort(key = getY)
        return [earth,planetList]

    def __init__(self):
        self.index = random.randint(0,2147483647)#I want these to be indicies but here I can assure they're unique which is a start
        self.resources = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
        self.size = random.lognormvariate(2,0.8)
        self.culture = OnlineMarkov()
        for i in range(-1,int(self.size*2/2)):
            cultureString = self.culture.randomString(int(self.size*2/2))
            #print(cultureString)
            self.culture.contribute(cultureString)
        self.position = [random.normalvariate(0,400),random.normalvariate(0,200),random.normalvariate(0,75)]

    def step(self):
        pass
        #if self.resources[1]<1:
        #    if self.resources[0]>1:
        #        self.resources[0] -= 
            

    def draw(self,win,reflect,screenCenter,yscaling,zscaling):
        planetColor = (self.resources[0],self.resources[1],self.resources[2])
        self.pos = (int(screenCenter[0]+self.position[0]),int(screenCenter[1]+yscaling*self.position[1]+zscaling*self.position[2]))
        proj = (int(screenCenter[0]+self.position[0]),int(screenCenter[1]+yscaling*self.position[1]))

        pygame.draw.line(win,(64,64,64),self.pos,proj)
        aafilledcircle(win,self.pos,self.size,planetColor)

        self.npos =  (int(screenCenter[0]+self.position[0]),int(screenCenter[1]+yscaling*self.position[1]-zscaling*self.position[2]))
        dimColor = (self.resources[0]*0.25,self.resources[1]*0.25,self.resources[2]*0.25)

        if(self.position[2]>0):
            pygame.draw.line(reflect,(16,16,16),self.npos,proj)
            aafilledcircle(reflect,self.npos,self.size,dimColor)

    def collidepoint(self,mousePos):
        if(magnitude(sub(self.pos,mousePos))<self.size):
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