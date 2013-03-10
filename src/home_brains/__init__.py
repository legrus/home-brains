import logging
import sys

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

from variable import Variable

from shell_source import ShellSource
from web_source import WebSource

from pipe import Pipe
from and_pipe import AndPipe
from xpath_pipe import XpathPipe

from gpio_sink import GpioSink
