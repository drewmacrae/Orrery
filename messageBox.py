import pygame
import random

class MessageBox:
    messageBoxFontSize = 18
    messageBoxspacing = 18
    #display messageBox in the upper right
    pygame.font.init()
    myfont = pygame.font.Font('OpenSans-Regular.ttf', messageBoxFontSize)
    def __init__(self,screenSize):
        self.talkstring = ">"
        self.screenSize = screenSize
        self.messages = ""
    def displayMessages(self,win,tickTime):
        textsurface = self.myfont.render(self.talkstring, True,(255,255,255))
        win.blit(textsurface,(self.screenSize[0]-258,0))
        
        messageList = self.messages.split("\n")
        if(len(messageList)>20):
            messageList = messageList[-20:]#take only the end of the messageList
        if(len(self.messages)>4000):
            self.messages = self.messages[-4000:]
        if random.randint(0,30000)<tickTime:
            self.messages = self.messages[-int(len(self.messages)*0.71):]
        offset = 0#FIXME right should work but I'm getting an empty thing from the listself.messageBoxspacing;
        for eachMessage in messageList[::-1]:
            textsurface = self.myfont.render(eachMessage, True,(255,255,255))
            win.blit(textsurface,(self.screenSize[0]-258,offset))
            offset += self.messageBoxspacing
