# simple first tests

from home_brains import *

x = ShellSource("echo 0")
w = WebSource("http://export.yandex.ru/bar/reginfo.xml")
err = WebSource("http://zzz.yandex.ru/bar/reginfo.xml")


traffic = XpathPipe([w], "string(/info/traffic/level)")
temperature = XpathPipe([w], "string(/info/weather/day/day_part[1]/temperature)")

# say it's summer if current temperature > 0
summer = ExpressionPipe([temperature, x], "{0} > {1}")

err2 = XpathPipe([err], "string(/info/weather/day/day_part[1]/temperature)")

# set the yellow led on of it's summer
gpio8 = GpioSink([summer], 8)


x.process()
w.process()
err.process()

traffic.process()
temperature.process()
summer.process()
err2.process()
gpio8.process()