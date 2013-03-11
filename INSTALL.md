Installation instructions
===========

0. Install prerequisites:
    + apt-get install libxml2-dev libxslt1-dev python-lxml
    + ~~pip install lxml~~ this caused errors for me
    + pip install RPi.GPIO

1. If you're on Pi, uncomment all GPIO-related lines in src/home_brains/gpio_sink.py

2. Adjust traffic.py to your needs and run it!
