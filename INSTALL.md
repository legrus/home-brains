Installation instructions
===========

0. Install prerequisites:
    + XML parsing:
        ~~pip install lxml~~ this caused errors for me
        apt-get install libxml2-dev libxslt1-dev python-lxml python-pyaudio
    + Raspberry Pi GPIO library
        pip install RPi.GPIO
    + MongoDB for logging
        https://github.com/RickP/mongopi    # on Pi


1. If you're on Pi, change DummyRPi module to a real one in [src/home_brains/gpio_sink.py](https://github.com/legrus/home-brains/blob/master/src/home_brains/gpio_sink.py)

2. Adjust examples in [src/](https://github.com/legrus/home-brains/blob/master/src/) example to your needs and run it!
