from home_brains import *

# Simple first tests


# First create some data sources to play with:
# An xml with recent weather and traffic reports
web = WebSource("http://export.yandex.ru/bar/reginfo.xml")

# Now specify how to extract data from the xml
traffic = XpathPipe([web], "string(/info/traffic/level)")
temperature = XpathPipe([web], "string(/info/weather/day/day_part[1]/temperature)")

# Now create three boolean variables for traffic density
light_traffic = ExpressionPipe([traffic], "{0} < 4")
moderate_traffic = ExpressionPipe([traffic], "{0} >= 4 and {0} <= 6")
heavy_traffic = ExpressionPipe([traffic], "{0} > 6")


# Finally set the output ("sinks"): the yellow led is on of it's summer
gpio9 = GpioSink([light_traffic], 9)
gpio8 = GpioSink([moderate_traffic], 8)
gpio7 = GpioSink([heavy_traffic], 7)



# Check how do we deal with nonexistent urls
# err = WebSource("http://zzzzzzzzzzzzzzzzzzzz.yandex.ru")
# err2 = XpathPipe([err], "string(/info/weather/day/day_part[1]/temperature)")
# err.process()
# err2.process()



# Now as we are set up, run the circuit once.
# In production you would like to set time intervals or triggers for it.
web.process()

traffic.process()
temperature.process()

light_traffic.process()
moderate_traffic.process()
heavy_traffic.process()

gpio7.process()
gpio8.process()
gpio9.process()
