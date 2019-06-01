import pygame
import random
import string
import math
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

def normalize(vector):
    sumOfSquares = 0
    result = [0]*(len(vector))
    for eachComponent in vector:
        sumOfSquares = sumOfSquares+eachComponent**2
    magnitude = math.sqrt(sumOfSquares)
    for eachIndex in range(len(vector)):
        result[eachIndex]=vector[eachIndex]/magnitude
    return result

def sub(vectorA,vectorB):
    return add(scale(-1,vectorB),vectorA)

def add(vectorA,vectorB):
    assert len(vectorA)==len(vectorB)
    result = [0]*(len(vectorA))
    for eachIndex in range(len(vectorA)):
        result[eachIndex] = vectorA[eachIndex]+vectorB[eachIndex]
    return result

def magnitude(vector):
    #print("computingMagnitude of")
    #print(vector)
    sumOfSquares = 0
    for eachComponent in vector:
        sumOfSquares = sumOfSquares+eachComponent**2
    magnitude = math.sqrt(sumOfSquares)
    #print(magnitude)
    return magnitude

def scale(scalar,vectorA):
    result = [0]*(len(vectorA))
    for eachIndex in range(len(vectorA)):
        result[eachIndex] = vectorA[eachIndex]*scalar
    return result

class FPSDisplay:
    #display FPS in upper left. I thought it was slow and wanted to check to see if it really was
    pygame.font.init()
    myfont = pygame.font.SysFont('Courier MS', 12)
    def displayFPS(self):
        textsurface = self.myfont.render(str(clock.get_fps())[:5], False, (255, 255, 255))
        win.blit(textsurface,(0,0))

depletionRate = 0.01

class planet:
    def __init__(self):
        self.resources = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
        self.size = random.lognormvariate(2,0.8)
        self.culture = {}
        self.position = [random.normalvariate(0,400),random.normalvariate(0,200),random.normalvariate(0,100)]
    def draw(self):
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
        
class player:
    position = [500.0,500.0,0.0]
    resources = [255.0,255.0,255.0]
    target = None
    at = None
    velocity = 0.05
    def step(self):
        assert(tickTime>0)
        
        if self.resources[1]>1:
            self.resources[1]-=tickTime*depletionRate
            assert(self.resources[1]<255)
        else:
            self.resources[0]-=tickTime*depletionRate
            
        if self.target!=None:
            self.at = None
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

            print(self.at.resources)
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

def getY(srcobject):
    return srcobject.position[1]
    
#instantiate local planets
earth = planet()
earth.size = 10
earth.position = [0.0,0.0,0.0]
earth.resources = [32.0,192.0,128.0]
planets = [earth]

for i in range(40):
    planets = planets+[planet()]

planets.sort(key = getY)

myPlayer = player()
myPlayer.target = earth

pygame.mixer.music.load('3. Mercury.ogg')
pygame.mixer.music.play()

while run:
    win.fill((0,0,0))
    #timing
    tickTime = clock.tick()
    fps.displayFPS()

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
    
    keys = pygame.key.get_pressed()

    #MODEL
    myPlayer.step()
    
    #VIEW
    #draw planets
    for eachPlanet in planets:
        eachPlanet.draw()
    #draw player
    pos = (int(screenCenter[0]+myPlayer.position[0]),int(screenCenter[1]+yscaling*myPlayer.position[1]+zscaling*myPlayer.position[2]))
    proj = (int(screenCenter[0]+myPlayer.position[0]),int(screenCenter[1]+yscaling*myPlayer.position[1]))
    pygame.draw.line(win,(32,32,32),pos,proj)
    pygame.draw.rect(win,(myPlayer.resources[0],myPlayer.resources[1],myPlayer.resources[2]),(pos[0],pos[1],width,height))
    myPlayer.draw()

    pygame.display.update()

pygame.quit()
