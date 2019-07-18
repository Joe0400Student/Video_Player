
import Widgets
import pygame
import vlc
from singleton_decorator import singleton
import hachoir
import platform
import ctypes
from enum import IntEnum
import config

#
#   TODO: find out how in the world the callbacks in this case work, and what it asks of the memory
#
#


class Movement(IntEnum):
    UP = 1
    DOWN = 0

CorrectVideLockCb = ctypes.CFUNCTYPE(ctypes.c_void_p,
                                     ctypes.c_void_p,
                                     ctypes.c_void_p,
                                     ctypes.POINTER(
                                         ctypes.c_void_p
                                     ))
CorrectVideoUnlockCb = ctypes.CFUNCTYPE(ctypes.c_void_p,
                                         ctypes.c_void_p,
                                         ctypes.POINTER(
                                             ctypes.c_void_p
                                         ))
CorrectVideoDisplayCb = ctypes.CFUNCTYPE(ctypes.c_void_p,
                                         ctypes.c_void_p,
                                         ctypes.POINTER(
                                             ctypes.c_void_p
                                         ))


@singleton
class Movie:

    mutexL = False
    

    def __init__(self,x,y,videoID,video: str):
        self.widgets = Widgets.Widgets()
        self.instance = vlc.Instance()
        self.media = None
        self.player = None
        self.videoID = videoID
        self.len = None
        self.system = platform.system()
        self.tick = 0
        self.mousemove = 0
        self.x = x / 2 - 768 / 2
        self.y = y
        self.pos = Movement.UP
        self.controlYPosTop = y-266
        self.controlYpos = y-256
        self.playing = True
        global callbackPointer
        callbackPointer = ctypes.POINTER(ctypes.c_int)()
        global savedBuffer
        savedBuffer = (ctypes.c_ubyte * x * y * 4)()
        global bufferpointer
        bufferpointer = ctypes.cast(self.savedBuffer, ctypes.c_void_p)


    @CorrectVideLockCb
    def mutexLock(opaque,planes):
        planes[0] = bufferpointer

    @CorrectVideoDisplayCb
    def display(a,b):
        img = pygame.image.frombuffer(savedBuffer,(1920,1080),"RGBA")


    def firstPlay(self, video:str):
        self.media = self.instance.media_new(video)
        self.player = self.instance.media_player_new()
        if self.system in ['Linux', 'Darwin']:
            print("Linux Or Darwin")
            self.player.set_xwindow(self.videoID)
        else:
            self.player.set_hwnd(self.videoID)
        self.player.set_media(self.media)

        self.player.video_set_callbacks(self.mutexLock,None,self.display,None)
        pygame.mixer.quit()
        self.player.play()
        self.len = self.media.get_duration()
        print("{} len".format(self.len))

    def backOut(self):
        self.player.stop()
        self.player = None
        self.media = None
        self.len = None
        pygame.mixer.music.init()

    def drawMovie(self, screen: pygame.Surface,event: list,movie: str,
                  mouseclicked: bool,mousepos: tuple):
        for e in event:
            if e.type == pygame.MOUSEMOTION:
                self.mousemove = self.tick
                self.pos = Movement.UP
        if self.player is None:
            self.firstPlay(movie)
        if self.pos == Movement.UP and self.controlYpos > self.controlYPosTop:
            self.controlYpos -= 5
        elif self.pos == Movement.UP and self.controlYpos < self.controlYPosTop:
            self.controlYpos = self.controlYPosTop
        if self.pos == Movement.DOWN and self.controlYpos < self.y:
            self.controlYpos += 5
        if self.pos == Movement.UP and self.mousemove + 50 == self.tick:
            self.pos = Movement.DOWN
        self.playing , rect = self.widgets.player(screen,self.x,self.controlYpos,mouseclicked,mousepos,
                                                self.pauseToggle,self.skipBack,self.skipforwards,movie,
                                               self.playing,self.getPos(),self.len,self.setPos,self.skipBack)

        pygame.display.update(rect)
        self.tick += 1

    def pauseToggle(self):
        self.player.pause()

    def skipforwards(self):
        print("skip ahead")

    def skipBack(self):
        print("skip back")

    def skipTo(self, pos: int):
        self.player.set_position(pos/self.len)

    def getPos(self):
        a = self.player.get_time()
        if a != 0:
            return a
        else:
            return 1

    def setPos(self,pos: int):
        self.player.set_position(pos/self.len)
