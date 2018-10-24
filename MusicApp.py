import pygame

class MusicApp:

    def __init__(self, *args):
        self.playlist = []
        self.songs = []
        for song in args:
            self.songs.append(song)
        pygame.mixer.init(frequency=26050,size=-16,channels=2,buffer=4096)
        self.offset = 0
        self.play = False
        self.playable = False
        self.pos = 0
        self.offset = 0
        self.length = 1
        self.songName = None

    def playSong(self,song: str,pos:int):
        pygame.mixer.music.stop()
        pygame.mixer.music.play(song,pos)
        if self.playing:
            pygame.mixer.music.pause()
        self.songName = song
        self.offset = pos*1000


    def addPlaylist(self,song: str):
        if song in self.songs:
            self.playlist.append(song)
            if self.playable == False:
                self.playSong(str)
            self.playable = True
            return True
        return False

    def removePlaylist(self,song: str):
        if len(self.playlist) != 0:
            if song in self.playlist:
                pos = self.playlist.index(song)
                self.playlist.remove(song)
                if pos == self.pos:
                    pygame.mixer.music.stop()
                    self.offset = 0
                    pygame.mixer.music.play(self.playlist[self.pos])
                    if not self.playing:
                        pygame.mixer.music.pause()
                return True

    def togglePlay(self):
        if self.playable:
            if self.play:
                pygame.mixer.music.pause()
                self.play = False
            else:
                pygame.mixer.music.unpause()
                self.play = True


    def skipAhead(self):
        if self.playable:
            if self.pos + 1 < len(self.playlist):
                self.pos += 1
                pygame.mixer.music.stop()
                pygame.mixer.music.play(self.playlist[self.pos])
                if not self.play:
                    pygame.mixer.music.pause()


    def seek(self,pos: float):
        if self.songName is not None:
            self.playSong(self.songName)
            if not self.play:
                pygame.mixer.music.pause()
            self.offset = pos*1000


