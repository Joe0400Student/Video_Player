from setuptools import setup

setup(
    name='OpenVideoPlayer',
    description='A Open Source, Free Domain Video Player',
    author='Joseph Scannell',
    version='Alpha 0.0.0',
    scripts=['Music','Menu','Movie','MusicApp','Settings','SoundConverter','Widgets','YoutubeDownloader'],
    install_requires=[
        'pygame','python-vlc','singleton-decorator','psutil','gmusicapi'
    ]
)