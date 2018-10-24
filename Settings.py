from Widgets import Widgets
import pygame
import os
from singleton_decorator import singleton

@singleton
class Settings:

    def __init__(self):
        self.file = None
        self.state = None
        self.saved = None
        self.openFile('settings.conf')
        self.GMT = None
        self.resx = None
        self.resy = None
        self.background = None
        self.backgroundType = None



    def generateSettings(self,resx: int, resy: int, backgroundType:bool,
                         background,GMT: bool, fontforPlayer: str,fontfortime:str):
        st = "settings:[\n\tresolution_x:{};\n\tresolution_y:{};\n\tbackground:".format(resx,resy)
        if backgroundType:
            r = background[0]
            g = background[1]
            b = background[2]
            st += "rgb({},{},{});\n\tGMT:{};\n\tplayerfont:".format(r,g,b,int(GMT))
        else:
            st += "img(\'{}\');\n\tGMT:{};\n\tplayerfont:".format(background,int(GMT))
        if fontforPlayer is "":
            st += "NULL;\n\tfontfortime:"
        else:
            st += "{};\n\tfontfortime:".format(fontforPlayer)
        if fontfortime is "":
            st += "NULL:\n]"
        else:
            st += "{};\n]".format(fontfortime)

        self.file.write(st)
        self.file.close()
        self.file = open('settings.conf','r+')
        self.state = 0

    def getSettings(self):
        self.saved = self.file.read()


    def openFile(self,location: str):
        try:
            self.file = open(location,'x')
            self.state = 0
        except FileExistsError:
            self.file = open(location,'r+')
            self.state = 1
            vinfo = pygame.display.Info()
            self.generateSettings(vinfo.current_w,vinfo.current_h,True,(64,64,255),True,'CooperHewitt-Light.otf','CooperHewitt-Medium.otf')
