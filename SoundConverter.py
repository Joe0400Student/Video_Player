import os
from pydub import AudioSegment

class SoundConverter:

    supportedType = ['mp3','wav','ogg']

    def __init__(self):
        self.files = os.listdir()

    def convert(self):
        f = open('Music.generated','w')
        s = ""
        for file in self.files:
            for type in SoundConverter.supportedType:
                if '.' + type in file and '.ogg' not in file:
                    AudioSegment.from_file(file,type).export(file[:-4],format='ogg')
                    s += file[:-4]+'.ogg,'
                elif 'ogg' in file:
                    s += file + ','
        f.write(s[:-1])
        f.close()
