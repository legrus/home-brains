#!/usr/bin/python
# -*- coding: UTF-8 -*-
# https://github.com/legrus/home-brains, legrus, 2013

import logging
import sys
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

from home_brains import *

circuit = Circuit("broadcast_example")

circuit.create('MicSource', 'mic', '', [], {})
circuit.create('RegexpPipe', 'dummy', '(.*)', ['mic'], {})
circuit.create('PlaySink', 'player', '', ['dummy'], {})

circuit.start_loop()
