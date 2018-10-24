from singleton_decorator import singleton
from enum import Enum as enum
from enum import IntEnum
import pygame
import Widgets
import multiprocessing as mp

class Movement(IntEnum):
    UP = -5
    DOWN = 5
    STOPPED = 0

class Position(IntEnum):

    VIDEO = 0
    MUSIC = 1
    GOOGLE_PLAY=2
    YOUTUBE=3
    SETTINGS=4


@singleton
class Menu:


    def __init__(self,x,y,surface:pygame.Surface):
        self.slideout = 0
        self.timestamp = 0
        self.prevtimestamp = -10
        self.size = (x,y)
        self.video = pygame.image.load('Video.png')
        self.settings = pygame.image.load('Settings.png')
        self.moving = Movement.STOPPED
        self.menuPos = Position.GOOGLE_PLAY
        self.Widgets = Widgets.Widgets()
        self.imgDrawSize = int((y-40)/5)
        self.boxpos = [self.imgDrawSize*i+45 for i in range(5)]
        self.pos = self.boxpos[int(self.menuPos)]
        self.imgDrawSize -= 10
        self.video = pygame.transform.scale(self.video,(self.imgDrawSize,self.imgDrawSize))
        self.settings = pygame.transform.scale(self.settings,(self.imgDrawSize,self.imgDrawSize))
        self.surf = surface
        self.update = True
        self.y = y

    def slideOut(self):
        if self.slideout - 5 <= -(self.imgDrawSize + 10):
            self.slideout = -(self.imgDrawSize + 10)
            return True
        else:
            self.slideout -= 5
            return False

    def slideIn(self):
        print(self.slideout)
        if self.slideout + 5 >= 0:
            self.slideout = 0
            self.update = True
            return True
        else:
            self.slideout += 5
            return False

    def drawMenu(self,event:list):
        c = None
        updateChange = False
        for e in event:
            if e.type == pygame.KEYDOWN and self.timestamp - self.prevtimestamp > 10:
                if e.key == pygame.K_RETURN:
                    c = self.menuPos
                elif e.key == pygame.K_DOWN:
                    if self.menuPos != 4:
                        print(self.menuPos)
                        self.menuPos += 1
                        print(self.menuPos)
                        self.moving = Movement.DOWN
                        self.prevtimestamp = self.timestamp
                        self.update = True
                elif e.key == pygame.K_UP:
                    print("k up")
                    if self.menuPos != 0:
                        self.menuPos -= 1
                        self.moving = Movement.UP
                        self.prevtimestamp = self.timestamp
                        self.update = True

        if self.moving < 0 and self.pos - self.moving <= self.boxpos[self.menuPos]-5 or \
                self.moving > 0 and self.pos + self.moving >= self.boxpos[self.menuPos]-5:
            self.pos = self.boxpos[self.menuPos]-5
            self.moving = 0
            updateChange = True
        self.pos += self.moving
        for i in range(4):
            self.surf.blit(self.video,(5+self.slideout,self.boxpos[i]))
        self.surf.blit(self.settings,(5+self.slideout,self.boxpos[4]))
        pygame.draw.rect(self.surf,(255,255,255),(self.slideout,self.pos,self.imgDrawSize+10,self.imgDrawSize+10),2)

        self.timestamp += 1
        d = None
        if self.update:
            d = (0, 40, self.imgDrawSize + 10, self.y - 40)
        if updateChange:
            self.update = False
        return c,d
