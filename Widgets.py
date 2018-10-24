import pygame
import datetime
from singleton_decorator import singleton
import psutil
from typing import Callable

@singleton
class Widgets:

    def __init__(self):
        self.month = ["January", "February", "March", "April",
                      "May", "June", "July", "August", "September",
                      "October", "November", "December"]
        self.weekday = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        self.MusicWidget = pygame.image.load('Widget.png')
        self.PlayButton = pygame.image.load('Play.png')
        self.Back = pygame.image.load('Back.png')
        self.pause = pygame.image.load('Pause.png')
        pygame.font.init()
        self.font = pygame.font.Font('CooperHewitt-Light.otf',92)
        self.timeFont = pygame.font.Font('CooperHewitt-Medium.otf',24)
        self.count = 1
        self.datetime = datetime.datetime.now()
        self.batcount = 1
        self.bat = psutil.sensors_battery()
        self.batteryFont = pygame.font.Font('CooperHewitt-Medium.otf',24)
        self.calls = 0
        self.prevcalls = -11
        self.previousclick = False
        self.back = False
        self.backb = pygame.image.load('backb.png')
        self.quitb = pygame.image.load('Quit.png')
        self.PlayerFont = pygame.font.Font(None,14)
        """ 
    
        :param screen is the screen that it applys to
        ;param x, y
        ;param clicked is for one overarching event handling system
        ;param mouse pso is the raw mouse position handeled
        ;param music_toggle, music_back, music_forwards are all functions that 
        are used to handel music/video playback
        ;param text is the name to display
        ;parma playing is telling the function whether or not to dsiplay that it 
        is playing(play button), or isnt(pause button)
        
        ;returns the state that the player is at, after 
    
    
    """

    def player(self, screen: pygame.Surface, x: int, y: int,clicked: bool,
                mousepos: tuple, music_toggle: Callable,music_back: Callable,
               music_forwards: Callable, text: str,playing: bool,pos:int,
               length:int,seek_function:Callable, rewind:Callable):
        screen.blit(self.MusicWidget, (x, y))
        if not playing:
            screen.blit(self.PlayButton, (x+320,y+128))
        else:
            screen.blit(self.pause,(x+320,y+128))
        screen.blit(self.PlayButton,(x+480,y+128))
        screen.blit(self.PlayButton,(x+552,y+128))
        screen.blit(self.Back,(x+160,y+128))
        screen.blit(self.Back,(x+96,y+128))
        newtext = self.generateTextToFit(text,768-40)
        txt = self.font.render(newtext,False,(0,0,0),(255,255,255))
        len = self.font.size(newtext)[0]
        screen.blit(txt,(x+768/2 - int(len/2),y+30))
        mousepsx = mousepos[0]
        if not self.previousclick:
            pygame.draw.rect(screen,(255,0,0),(x,y+108,pos/length*768,28))
        if self.previousclick:
            if x <= mousepsx <= x+768:
                pygame.draw.rect(screen,(255,0,0),(x,y+108,mousepos[0]-x,28))
            else:
                if mousepsx < x:
                    mouspsx = x+1
                elif mousepsx > x+768:
                    mouspsx = x+767
                clicked = False
                self.previousclick = False
        if not clicked and self.previousclick:
            self.previousclick = not self.previousclick
            seek_function(((mousepsx-x)/768)*length/1000)

        if clicked and self.previousclick:
            self.previousclick = True
            self.back = False
        elif clicked and not self.previousclick and (self.calls-self.prevcalls) > 20:
            mouseposx = mousepos[0]
            mouseposy = mousepos[1]
            if y+128 <= mouseposy <= y +256:
                if x+96 <= mouseposx <= x+288:
                    if self.back:
                        rewind()
                    else:
                        music_back()
                    self.back = True
                    self.prevcalls = self.calls
                elif x+320 <= mouseposx <= x+448:
                    music_toggle()
                    playing = not playing
                    self.back = False
                    self.prevcalls = self.calls
                elif x+480 <= mouseposx <= x+672:
                    music_forwards()
                    self.prevcalls = self.calls
                    self.back = False
            elif y+100 <= mouseposy < y+128:
                if x <= mouseposx <= x+768:
                    self.previousclick = True
                    self.back = False
        else:
            self.previousclick = False
        self.calls += 1
        pygame.display.update()
        return playing , (x,y,768,256)

    def generateTextToFit(self,text:str, length):

        if ' ' in text:
            while self.font.size(text)[0] > length:
                text = ' '.join(text.split(' ')[0:-1])+"..."
        else:
            while self.font.size(text)[0] > length:
                text = text[0:-1]
                text = text[0:-3] + '...'
        return text

    """
        This one is differenet, based on center of x, and the top is y
    """
    def drawTime(self,screen: pygame.Surface,x:int,y:int,color:tuple ,full: bool,GM:bool):
        upd = False
        if self.count % 100 == 0:
            upd = True
            self.datetime = datetime.datetime.now()
        date = self.datetime.date()
        Month = self.month[date.month]
        dayNum = date.day
        year = str(date.year)
        dayWeek = self.weekday[date.weekday()]
        dayNum = str(dayNum)
        time = self.datetime.time()
        hour = time.hour
        min = str(time.minute).zfill(2)
        pm = None
        if GM:
            pm = int(hour/12) == 0
            if hour % 12 == 0:
                pm = not pm
            hour = hour%12
            if hour == 0:
                hour = 12
        hour = str(hour)
        text = ""
        if full:
            text = dayWeek + " " + Month + " " + dayNum + "," + year + " " + hour + ":" + min
        else:
            text = dayWeek[0:3] + " " + Month[0:3] + " " + dayNum +"," +year+" " + hour + ":" + min
        if GM:
            if pm:
                text += " AM"
            else:
                text += " PM"
        w = self.timeFont.size(text)[0]
        r = self.timeFont.render(text,False,color,(0,0,0))
        screen.blit(r,(x-int(w/2),y))


        self.count += 1
        return upd

    def drawBattery(self,x,y,screen:pygame.Surface,color:tuple):
        upd = False
        if not self.batcount % 100:
            self.bat = psutil.sensors_battery()
            upd = True
        if self.bat is None:
            img = self.batteryFont.render("AC",False,color)
            nx, _ =self.batteryFont.size("AC")
            screen.blit(img,(x-nx,y))
        else:
            st = "{}%".format(int(self.bat.percent))
            nx , _ = self.batteryFont.size(st)
            img = self.batteryFont.render(st,False,color)
            screen.blit(img,(x-nx,y))
        self.batcount += 1
        return upd

    def drawTitleBar(self,x,y,screen:pygame.Surface,GMT:bool,mousepos:tuple,mouseclick:bool):
        pygame.draw.rect(screen,(0,0,0),(0,0,x,40))
        upd = self.drawTime(screen,x/2,10,(255,255,255),False,GMT)
        upd = upd or self.drawBattery(x-40,10,screen,(255,255,255))
        self.quit(x,0,screen,mousepos,mouseclick)
        if upd:
            return (0,0,x-30,40)

    def backButton(self,x,y,screen:pygame.Surface,mousepos:tuple,mouselclick:bool):
        screen.blit(self.backb,(x,y))
        if mouselclick:
            if x <= mousepos[0] <= x+30:
                if y<= mousepos[1] <= y+30:
                    return True, (x,y,30,30)
        return False, (x,y,30,30)
    def quit(self,x,y,screen:pygame.Surface,mousepos:tuple,mouseclick:bool):
        screen.blit(self.quitb,(x-30,y))
        if mouseclick:
            if x-30 <= mousepos[0] <= x:
                if y <= mousepos[1] <= y+30:
                    quit(0)

    def convetMStoTimeFormat(self,n: int):
        n /= 1000
        hour = n % 3600
        if hour > 0:
            n /= 3600
        min = n % 60
        if min > 0:
            n /= 60
        sec = n
        return "{}:{}:{3:2d}".format(hour,min,sec)