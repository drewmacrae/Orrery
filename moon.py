from planet import Planet
import random
import pygame
from vectormath import *
from onlineMarkov import OnlineMarkov
import pygame.gfxdraw
import math
import numpy as np

class Moon(Planet):
    def __init__(self,parent,control = "RANDOM"):
        self.parent = parent
        if(control=="LUNA"):
            self.initluna()
            return
        if(control=="PHOBOS"):
            self.initphobos()
            return
        if(control=="DEIMOS"):
            self.initdeimos()
            return
        if(control=="IO"):
            self.initio()
            return
        if(control=="EUROPA"):
            self.initeuropa()
            return
        if(control=="GANYMEDE"):
            self.initganymede()
            return
        if(control=="CALLISTO"):
            self.initcallisto()
            return
        if(control=="TITAN"):
            self.inittitan()
            return
        if(control=="TRITON"):
            self.inittriton()
            return
        if(control=="CHARON"):
            self.initcharon()
            return
        self.index = random.randint(0,2147483647)#I want these to be indicies but here I can assure they're unique which is a start
        self.resources = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
        self.size = random.lognormvariate(math.log(1.5),0.3)
        self.culture = OnlineMarkov()
        for i in range(-1,int(self.size*2/2)):
            cultureString = self.culture.randomString(int(self.size*2/2))
            #print(cultureString)
            self.culture.contribute(cultureString)
        self.radius = random.lognormvariate(math.log(parent.size*2),0.125)
        #print(self.radius)
        self.inclination = random.normalvariate(0,15)
        self.longitudeAscendingNode = random.uniform(0,360)
        self.trueAnomaly = random.uniform(0,360)
        self.period = Planet.getPeriodFromRadius(self.radius)
        self.rotationMatrix = Planet.eulerAngles2Matrix(self.inclination,self.longitudeAscendingNode)
        self.position = self.getPosition()
    def getPosition(self):
        #compute position in the plane of the orbit
        x = self.radius*math.sin(self.trueAnomaly*math.pi/180.0)
        y = self.radius*math.cos(self.trueAnomaly*math.pi/180.0)
        z = 0

        #ignore inclination and longitude of ascending node for now
        return add(self.parent.getPosition(),np.matmul(self.rotationMatrix,[x,y,z]))
    
    def initluna(self):
        self.size = 3
        self.radius = 20
        self.resources = [64.0,64.0,64.0]
        self.culture = OnlineMarkov()
        for i in range(-1,int(self.size*2/2)):
            cultureString = self.culture.randomString(int(self.size*2/2))
            #print(cultureString)
            self.culture.contribute(cultureString)
        self.trueAnomaly = 25
        self.period = Planet.getPeriodFromRadius(self.radius)
        self.inclination = 15
        self.longitudeAscendingNode = 150
        self.rotationMatrix = Planet.eulerAngles2Matrix(self.inclination,self.longitudeAscendingNode)
        self.position = self.getPosition()
    def initphobos(self):
        self.size = 2
        self.radius = 10
        self.resources = [64.0,64.0,64.0]
        self.culture = OnlineMarkov()
        for i in range(-1,int(self.size*2/2)):
            cultureString = self.culture.randomString(int(self.size*2/2))
            #print(cultureString)
            self.culture.contribute(cultureString)
        self.trueAnomaly = 151
        self.period = Planet.getPeriodFromRadius(self.radius)
        self.inclination = 5
        self.longitudeAscendingNode = 110
        self.rotationMatrix = Planet.eulerAngles2Matrix(self.inclination,self.longitudeAscendingNode)
        self.position = self.getPosition()
    def initdeimos(self):
        self.size = 1
        self.radius = 12
        self.resources = [64.0,64.0,64.0]
        self.culture = OnlineMarkov()
        for i in range(-1,int(self.size*2/2)):
            cultureString = self.culture.randomString(int(self.size*2/2))
            #print(cultureString)
            self.culture.contribute(cultureString)
        self.trueAnomaly = 274
        self.period = Planet.getPeriodFromRadius(self.radius)
        self.inclination = 16
        self.longitudeAscendingNode = 280
        self.rotationMatrix = Planet.eulerAngles2Matrix(self.inclination,self.longitudeAscendingNode)
        self.position = self.getPosition()

    def generateMoonList(planetList):
        [earth,mars,jupiter,saturn,uranus,neptune,pluto]=planetList
        luna = Moon(earth,"LUNA")
        phobos = Moon(mars,"PHOBOS")
        deimos = Moon(mars,"DEIMOS")
        #io = Moon(jupiter,"IO")
        #europa = Moon(jupiter,"EUROPA")
        #ganymede = Moon(jupiter,"GANYMEDE")
        #callisto = Moon(jupiter,"CALLISTO")
        #titan = Moon(saturn,"TITAN")
        #saturni = [Moon(saturn,"RANDOM")*7]
        #uranii = [Moon(uranus,"RANDOM")*6]
        #triton = Moon(neptune,"TRITON")
        #neptunii = [Moon(neptune,"RANDOM")*2]
        #charon = Moon(pluto,"CHARON")

        return [luna,phobos,deimos]#,io,europa,ganymede,callisto,titan]+saturni+uranii+[triton]+neptunii+[charon]
