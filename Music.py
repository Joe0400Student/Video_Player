from Widgets import Widgets
import gmusicapi
import pygame
import time
import Menu
import Movie

from enum import IntEnum

pygame.init()

gameDisplay = pygame.display.set_mode((1920,1080),pygame.FULLSCREEN)



pygame.display.set_caption('test')
song = 0
Widgets = Widgets()

screenw, screenh = pygame.display.Info().current_w, pygame.display.Info().current_h


class Music:
    SONG_END = pygame.USEREVENT + 1


    def __init__(self,songs: list):
        pygame.mixer.init(frequency=26050,size=-16,channels=2,buffer=8192)
        self.offset = 0
        self.songs = songs
        self.pos = 0
        self.timesCalled = 0
        self.playing = False
        pygame.mixer.music.load(songs[self.pos])
        pygame.mixer.music.play()
        pygame.mixer.music.pause()
        tmp = pygame.mixer.Sound(songs[0])
        self.length = tmp.get_length()*1000
        del tmp
        pygame.mixer.music.set_endevent(Music.SONG_END)

    def nextSong(self):
        if len(self.songs) > self.pos + 1:
            pygame.mixer.music.load(self.songs[self.pos+1])
            tmp = pygame.mixer.Sound(self.songs[self.pos+1])

            self.length = tmp.get_length()*1000
            del tmp
            self.pos += 1
            self.offset = 0
            if self.playing:
                pygame.mixer.music.play()

    def play(self):
        if not self.playing:
            pygame.mixer.music.unpause()
            self.playing = True
        else:
            pygame.mixer.music.get_pos()
            pygame.mixer.music.pause()
            self.playing = False


    def rewind(self):
        pygame.mixer.music.stop()
        if self.playing:
            pygame.mixer.music.play()
        self.offset=0
        self.timesCalled += 1

    def back(self):
        if self.pos > 0:
            pygame.mixer.music.load(self.songs[self.pos-1])
            self.length = pygame.mixer.Sound(self.songs[self.pos-1]).get_length()*1000
            self.offset=0
            self.pos -= 1
            pygame.mixer.music.play()
            if not self.playing:
                pygame.mixer.music.pause()

    def getPos(self):
        return self.offset + pygame.mixer.music.get_pos()

    def setPos(self,pos: float):
        pygame.mixer.music.stop()
        pygame.mixer.music.play(0,pos)
        if not playing:
            pygame.mixer.music.pause()
        self.offset = pos*1000
currenttime = time.time()
timestamp = 0
prevtimestamp = 0
isvisible = True
Music = Music(['Never Gonna Give You Up Original.ogg','Фабрика – Катюша (LIVE Авторадио).ogg','896851539807807.ogg'])
menu = Menu.Menu(screenw,screenh,gameDisplay)
CurrentMenu = None
playing = False
x,y = 100,100
mx, my = True,True
goback = False
bringup = False
rect = [None,None,None,None]
gameDisplay.fill((128,128,128))
pygame.display.flip()
upd = pygame.display.update
movie = None
setCount = 0
while True:
    gameDisplay.fill((128,128,128))
    pressed = pygame.mouse.get_pressed()[0]
    pos = pygame.mouse.get_pos()
    a = pygame.event.get()
    _ = Widgets.drawTitleBar(screenw, screenh, gameDisplay,True,pos,pressed)
    if isvisible:
        if CurrentMenu is not None:
            isvisible = not menu.slideOut()
            _, _ = menu.drawMenu(a)
        elif bringup:
            bringup = not menu.slideIn()
            _, _ = menu.drawMenu(a)
            goback = False
        else:
            CurrentMenu, _ = menu.drawMenu(a)
        rect[2] = None
    else:
        rect[1] = None
        goback , _ = Widgets.backButton(5,5,gameDisplay,pos,pressed)
    if goback:
        isvisible = True
        CurrentMenu = None
        bringup = True
    for event in a:
        if event.type == pygame.QUIT:
            pygame.quit()
            quit(0)
        if event.type == Music.SONG_END:
            Music.nextSong()
    songname = Music.songs[Music.pos]
    if CurrentMenu == Menu.Position.VIDEO:
        if setCount == 0:
            setCount += 1
            movie = Movie.Movie(screenw, screenh, pygame.display.get_wm_info()["window"], 'Dat Bass.avi')
        movie.drawMovie(gameDisplay,a,'Dat Bass.avi',pressed,pos)
    pygame.display.flip()
    temp, currenttime = currenttime, time.time()
    if 1/60 - 1/(currenttime-temp) > 0:
        time.sleep(1/60-1/(currenttime-temp))
    currenttime = time.time()
    print(1/(currenttime-temp),end=' fps\n')
    timestamp += 1