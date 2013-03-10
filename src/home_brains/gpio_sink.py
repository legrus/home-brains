import logging
#from RPi import GPIO
from home_brains import *

#GPIO.setmode(GPIO.BCM)

class GpioSink(Pipe):
    """Set Raspberry Pi GPIOs"""
    gpio = None

    def __init__(self, _inputs, _gpio):
        super(GpioSink, self).__init__(_inputs)
        self.gpio = _gpio

    def process(self):
        super(GpioSink, self).preprocess() # check inputs are sane

        if self.gpio is None or len(self.inputs) == 0:
            self.error = True

        if not self.error:
            self.value = self.inputs[0].value
#            GPIO.output(self.gpio, self.value)

        super(GpioSink, self).process()
