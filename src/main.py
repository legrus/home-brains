from home_brains import *

# Simple first tests
# First create some data sources to play with:

# A constant with an integer value
x = ShellSource("echo 10")

# An xml with recent weather and traffic reports
w = WebSource("http://export.yandex.ru/bar/reginfo.xml")

# Now specify how to extract data from the xml
traffic = XpathPipe([w], "string(/info/traffic/level)")
temperature = XpathPipe([w], "string(/info/weather/day/day_part[1]/temperature)")

# Say it's summer if current temperature > 10
summer = ExpressionPipe([temperature, x], "{0} > {1}")
winter = ExpressionPipe([temperature, x], "{0} <= {1}")


# Finally set the output ("sinks"): the yellow led is on of it's summer
gpio8 = GpioSink([summer], 8)
gpio9 = GpioSink([winter], 9)



# Check how we deal with nonexistent urls
err = WebSource("http://zzzzzzzzzzzzzzzzzzzz.yandex.ru")
err2 = XpathPipe([err], "string(/info/weather/day/day_part[1]/temperature)")



# Now as we are set up, run the circuit once.
# In production you would like to set time intervals or triggers for it.
x.process()
w.process()
err.process()

traffic.process()
temperature.process()
summer.process()
winter.process()
err2.process()
gpio8.process()
gpio9.process()
