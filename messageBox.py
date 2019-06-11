import pygame
import random

class Message:
    def __init__(self,text,color):
        self.text = text
        self.color = color

class MessageBox:
    messageBoxFontSize = 18
    messageBoxspacing = 18
    messageLines = 20
    #display messageBox in the upper right
    pygame.font.init()
    myfont = pygame.font.Font('OpenSans-Regular.ttf', messageBoxFontSize)
    def __init__(self,screenSize):
        self.talkstring = ">"
        self.screenSize = screenSize
        self.messages = []
    def displayMessages(self,win,tickTime,playerColor):
        textsurface = self.myfont.render(self.talkstring, True,playerColor)
        win.blit(textsurface,(self.screenSize[0]-258,0))

        if(len(self.messages)>self.messageLines):
            self.messages = self.messages[-self.messageLines:]#take only the end of the messageList
        if random.randint(0,30000)<tickTime:#every 30sish trim messages
            self.messages = self.messages[-int((len(self.messages)-1)*0.71):]
        offset = self.messageBoxspacing
        for eachMessage in self.messages[::-1]:
            textsurface = self.myfont.render(eachMessage.text, True,eachMessage.color)
            win.blit(textsurface,(self.screenSize[0]-258,offset))
            offset += self.messageBoxspacing
