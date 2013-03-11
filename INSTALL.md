Installation instructions
===========

0. Install prerequisites:
    + apt-get install libxml2-dev libxslt1-dev python-lxml
    + ~~pip install lxml~~ this caused errors for me
    + pip install RPi.GPIO

1. If you're on Pi, change DummyRPi module to a real one in https://github.com/legrus/home-brains/blob/master/src/home_brains/gpio_sink.py

2. Adjust https://github.com/legrus/home-brains/blob/master/src/traffic.py example to your needs and run it!
