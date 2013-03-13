#!/usr/bin/python
# -*- coding: UTF-8 -*-
# https://github.com/legrus/home-brains, legrus, 2013

from home_brains import *


# This is not an example, but what I now run in my pi-powered house

circuit = Circuit("broadcast_example")
circuit.create('WebSource', 'wiki', 'http://en.wikipedia.org/wiki/Special:Random', [], {'period': 15, 'transient': True})
# Now specify how to extract data from the wiki page
circuit.create('XpathPipe', 'get_title', 'string(.//h1/span)', ['wiki'], {})
# Then convert the words to the sound file
circuit.create('SpeakingPipe', 'media', '', ['get_title'], {})
#circuit.create('ConstSource', 'file', '/tmp/speak-media.mp3', [], {'period': 5 * 60, 'transient': True})
#And just broadcast it!
circuit.create('FmSink', 'fm', '102.5', ['media'], {})


# First create some data sources to play with:
# A variable which evaluates to 1 if google.com is accessible
circuit.create('ShellSource', 'online', 'ping google.com -c 1 | grep "1 received" | wc -l', [], {'period': 60})
# An xml with recent weather and traffic reports
circuit.create('WebSource', 'yandex', 'http://export.yandex.ru/bar/reginfo.xml', [], {'period': 5 * 60, 'transient': True})
# Now specify how to extract data from the xml
circuit.create('XpathPipe', 'traffic', 'string(/info/traffic/level)', ['yandex'], {})
circuit.create('XpathPipe', 'temperature', 'string(/info/weather/day/day_part[1]/temperature)', ['yandex'], {})
# Now create three boolean variables for traffic density
circuit.create('ExpressionPipe', 'light_traffic', '{0} < 4', ['traffic'], {})
circuit.create('ExpressionPipe', 'moderate_traffic', '{0} >= 4 and {0} <= 6', ['traffic'], {})
circuit.create('ExpressionPipe', 'heavy_traffic', '{0} > 6', ['traffic'], {})
# Finally set the output ("sinks"): the red led on gpio7 for heavy traffic and vice versa
circuit.create('GpioSink', 'gpio9', 9, ['light_traffic'], {})
circuit.create('GpioSink', 'gpio8', 8, ['moderate_traffic'], {})
circuit.create('GpioSink', 'gpio7', 7, ['heavy_traffic'], {})
circuit.create('GpioSink', 'gpio11', 11, ['online'], {})


circuit.start_loop()
