# simple first tests

from home_brains import *

x = ShellSource("echo 1")
y = ShellSource("echo 1")
w = WebSource("http://export.yandex.ru/bar/reginfo.xml")
err = WebSource("http://zzz.yandex.ru/bar/reginfo.xml")


a = AndPipe([x, y])
traffic = XpathPipe([w], "string(/info/traffic/level)")
temperature = XpathPipe([w], "string(/info/weather/day/day_part[1]/temperature)")

err2 = XpathPipe([err], "string(/info/weather/day/day_part[1]/temperature)")

gpio8 = GpioSink([a], 8)


x.process()
y.process()
w.process()
err.process()

a.process()
traffic.process()
temperature.process()
err2.process()
#gpio8.process()