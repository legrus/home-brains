import logging

class GPIO(object):
    """
    A placeholder class to run tests outside real Raspberry Pi
    """

    @staticmethod
    def setup(pin, mode):
        logging.debug("DummyRPi::setup(%s, %s)", pin, mode)

    @staticmethod
    def output(pin, value):
        logging.debug("DummyRPi::output(%s, %s)", pin, value)

    @staticmethod
    def setmode(mode):
        logging.debug("DummyRPi::setmode(%s)", mode)

    BCM="BCM"
    OUT="OUT"
