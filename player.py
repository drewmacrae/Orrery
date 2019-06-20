from vectormath import *
import pygame
from messageBox import MessageBox
from messageBox import Message
import random

depletionRate = 0.005
greenDepletionRate = depletionRate/2        

class Player:
    def __init__(self,planets,msgs):
        self.planets = planets
        self.msgs = msgs
        self.position = [200.0,200.0,0.0]
        self.resources = [255.0,255.0,255.0]
        self.target = None
        self.at = None
        self.velocity = 0.05
    def talk(self,string):
        if self.at!=None:
            #if n and n.isConnected():
            #    n.talk(self.at.index,string)
            #else:
            self.at.talk(string)
            #endelse
            print(string)
            self.msgs.messages+=[Message(">"+string,self.resources)]
                

    def updateResources(self,tickTime):
        #use up green resources
        if self.resources[1]>0:
            self.resources[1]-=tickTime*greenDepletionRate
            if self.resources[1]<0:
                self.resources[1]=0
            assert(self.resources[1]<255)
        else:
            #if we're out of green then red runs out
            self.resources[0]-=tickTime*depletionRate
            if self.resources[0]<0:
                pygame.quit()
                exit()
        if self.target!=None:
            #we have a target so we're travelling so we use up blue resources    
            if self.resources[2]>0:
                self.resources[2]-=tickTime*depletionRate
                if self.resources[2]<0:
                    self.resources[2]=0
                assert(self.resources[2]<255)
            else:
                #if we're out of blue then red runs out
                self.resources[0]-=tickTime*depletionRate
                if self.resources[0]<0:
                       pygame.quit()
                       exit()
        if self.at != None:
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
            exit()

    def step(self, tickTime):
        if(tickTime == 0):
            return
        assert(tickTime>0)

        self.updateResources(tickTime)
    
        if self.target!=None:
            if self.at!=None:
                #departing
                self.at = None
                #if n and n.isConnected():
                #    n.depart()
                #Thank you to Soughtaftersounds at freesound for the music box
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('145434_2615119-lq.ogg'))
                #"Copyright © 2011 Varazuvi™ www.varazuvi.com"

            self.velocity = self.resources[2]/255*0.08

            #AUTOMATIC TRAVEL
            Vector2Target = sub(self.target.position,self.position)
            self.position = add(self.position,scale(self.velocity*tickTime,normalize(Vector2Target)))
            if magnitude(Vector2Target)<self.target.size:
                self.at = self.target
                self.target=None
                #arriving
                #if n and n.isConnected():
                #    n.arrive(self.at.index)
                #    response = n.listen(self.at.index)
                #else:
                response = self.at.listen()
                #endelse
                print(response)
                self.msgs.messages+=[Message(response,self.at.resources)]
                #Thank you to Soughtaftersounds at freesound for the menu sparkle
                #https://freesound.org/people/Soughtaftersounds/sounds/145459/
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('145459_2615119-lq.ogg'))

        if self.at != None:
            #We're at a planet, listen to what it has to say
            if random.randint(0,10000)<tickTime:
                #if n and n.isConnected():
                #response = n.listen(self.at.index)
                #else:
                response = self.at.listen()
                #endelse
                print(response)
                self.msgs.messages+=[Message(response,self.at.resources)]
                #Thank you to jotliner at freesound for the quindar tone!
                pygame.mixer.Channel(0).play(pygame.mixer.Sound('200813_2585050-lq.ogg'))


    def draw(self,win,screenSize):
        pygame.draw.rect(win,(255,10,10),(0,screenSize[1]-30,258,10))
        pygame.draw.rect(win,(10,255,10),(0,screenSize[1]-20,258,10))
        pygame.draw.rect(win,(10,10,255),(0,screenSize[1]-10,258,10))
        pygame.draw.rect(win,(10,10,10),(256,screenSize[1]-29,-254+self.resources[0],8))
        pygame.draw.rect(win,(10,10,10),(256,screenSize[1]-19,-254+self.resources[1],8))
        pygame.draw.rect(win,(10,10,10),(256,screenSize[1]-9,-254+self.resources[2],8))
