import logging
# -*- coding: UTF-8 -*-
# https://github.com/legrus/home-brains, legrus, 2013

from home_brains import *

# uncomment next line on a real RPi device
#from RPi import GPIO
from dummy_rpi import GPIO

GPIO.setmode(GPIO.BCM)

class GpioSink(Pipe):
    """Set Raspberry Pi GPIOs"""

    def gpio(self):
        return self.param

    def process(self):
        super(GpioSink, self).preprocess() # check inputs are sane

        if self.gpio() is None or len(self.inputs) == 0:
            self.error = True

        if not self.error and self.inputs[0].value is not None:
            self.value = bool(int(self.inputs[0].value))
            GPIO.output(self.gpio(), self.value)

        super(GpioSink, self).process()
