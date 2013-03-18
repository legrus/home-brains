Installation instructions
===========

1. Install prerequisites:
    + XML parsing:
        ~~pip install lxml~~ this caused errors for me
        apt-get install libxml2-dev libxslt1-dev python-lxml
    + Audio processing:
        apt-get install python-pyaudio flac ffmpeg mplayer
    + Raspberry Pi GPIO library (only if you're on a Pi)
        pip install RPi.GPIO
    + Handy for T2S
        pip install guess-language
    + MongoDB for logging
        https://github.com/RickP/mongopi    # on Pi


2. Adjust examples in [src/](https://github.com/legrus/home-brains/blob/master/src/) example to your needs and run it!
