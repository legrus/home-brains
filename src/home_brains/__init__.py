# -*- coding: UTF-8 -*-
# https://github.com/legrus/home-brains, legrus, 2013

__author__ = 'Oleg Petukhov'
__version__ = '0.1'


from variable import Variable

from const_source import ConstSource
from mic_source import MicSource
from shell_source import ShellSource
from web_source import WebSource

from and_pipe import AndPipe
from expression_pipe import ExpressionPipe
from speaking_pipe import SpeakingPipe
from regexp_pipe import RegexpPipe
from xpath_pipe import XpathPipe

from fm_sink import FmSink
from gpio_sink import GpioSink
from play_sink import PlaySink


# These types can be instantiated by Circuit.create()
VariableTypes = {
    "Variable": Variable,
    "ConstSource": ConstSource,
    "MicSource": MicSource,
    "ShellSource": ShellSource,
    "WebSource": WebSource,
    "AndPipe": AndPipe,
    "ExpressionPipe": ExpressionPipe,
    "SpeakingPipe": SpeakingPipe,
    "RegexpPipe": RegexpPipe,
    "XpathPipe": XpathPipe,
    "FmSink": FmSink,
    "GpioSink": GpioSink,
    "PlaySink": PlaySink
}

__all__ = VariableTypes.keys() + ['Circuit']

from circuit import Circuit
