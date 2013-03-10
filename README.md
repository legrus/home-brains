home-brains
===========

Smart things for my RaspberryPi-powered home.



Basic idea: create a virtual circuit of Sources, Pipes ans Sinks, e.g.

    WebSource (reading a weather forecast xml each hour)
    |
    +-- XpathPipe (extracting rain info from the XML)
        |
        +-- GpioSink (blinking blue LED connected to GPIO if I should take my umbrella)