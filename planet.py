import random
import pygame
from vectormath import *

class Planet:
    def __init__(self):
        self.resources = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
        self.size = random.lognormvariate(2,0.8)
        self.culture = {}
        self.position = [random.normalvariate(0,400),random.normalvariate(0,200),random.normalvariate(0,100)]
    def draw(self,win,screenCenter,yscaling,zscaling):
        planetColor = (self.resources[0],self.resources[1],self.resources[2])
        self.pos = (int(screenCenter[0]+self.position[0]),int(screenCenter[1]+yscaling*self.position[1]+zscaling*self.position[2]))
        proj = (int(screenCenter[0]+self.position[0]),int(screenCenter[1]+yscaling*self.position[1]))
        pygame.draw.line(win,(32,32,32),self.pos,proj)
        pygame.draw.circle(win,planetColor,self.pos,int(self.size))
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
