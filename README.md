home-brains
===========

Smart things for my RaspberryPi-powered home.



Basic idea: create a virtual circuit of Sources, Pipes ans Sinks, e.g.

    WebSource (reading a weather forecast xml each hour)
    |
    +-- XpathPipe (extracting rain info from the XML)
        |
        +-- GpioSink (blinking blue LED connected to GPIO if I should take my umbrella)

Logical elements and variables inspired by EPICS system, but I want more lightweight
solution in pure Python.

All logical circuit elements are called Variables and can be of three major types:

+ Source (periodical / triggered)
  * WebSource (fetches data from the web)
  * GpioSource (checks RaspberryPi GPIO pin input high/low state)
  * ShellSource (runs shell command, e.g. 'cat /proc/cpuinfo | grep MHz')

+ Pipe (has multiple Sources or other Pipes as inputs)
  * ExpressionPipe (evaluates arbitrary expression like "%1 > %2" over its inputs)
  * XpathPipe (extracts its value from given XML/HTML)

+ Sink (is actually a Pipe with one input and some physical side-efects)
  * GpioSink (sets RaspberryPi GPIO pins to blink leds, sound alarms, etc)
  * MessageSink (sends notifications)
    - EmailSink
    - SmsSink
    - SpeechSink
