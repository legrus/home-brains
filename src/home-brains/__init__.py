import logging
import sys

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

from variable import Variable

from shell_input import ShellInput
from web_input import WebInput

from pipe import Pipe
from and_pipe import AndPipe
from xpath_pipe import XpathPipe

from gpio_sink import GpioSink
