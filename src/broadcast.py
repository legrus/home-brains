#!/usr/bin/python
# -*- coding: UTF-8 -*-
# https://github.com/legrus/home-brains, legrus, 2013

import logging
import sys
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

from home_brains import *

# In this example we will read out a random word to an FM radio.
# It is backed up by a whole bunch of online resources, so this example might
# stop working at any moment.
# Random word generation depends on wikipedia markup.
# Text-to-speech is performed by google (unofficially)
# Audio conversion requires ffmpeg binaries on your system.
# Fm transmission depends on PiFM project

# This is our playground, virtual circuit board with signal sources, pipes and sinks
circuit = Circuit("broadcast_example")

# First create some data sources to play with:
circuit.create('WebSource', 'wiki', 'http://en.wikipedia.org/wiki/Special:Random', [], {'period': 15, 'transient': True})

# Now specify how to extract data from the wiki page
circuit.create('XpathPipe', 'get_title', 'string(.//h1/span)', ['wiki'], {})

# Then convert the words to the sound file
circuit.create('SpeakingPipe', 'media', '', ['get_title'], {})

#And just broadcast it!
circuit.create('FmSink', 'fm', '102.5', ['media'], {})


# Now the virtual circuit looks like this:
#
# wiki ---> get_title ---> media ---> fm


# Start the processing loop!
circuit.start_loop()
