import pygame

class FPSDisplay:
    #display FPS in upper left. I thought it was slow and wanted to check to see if it really was
    pygame.font.init()
    myfont = pygame.font.SysFont('Courier MS', 14)
    def displayFPS(self,win,clock):
        textsurface = self.myfont.render(str(clock.get_fps())[:5], True, (255, 255, 255))
        win.blit(textsurface,(0,0))
        pass