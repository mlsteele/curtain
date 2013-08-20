import time, os, math
from curtain import Curtain, frame_length
from plugin import Plugin
from plugins.strobe import Strobe
from plugins.rainbow import Rainbow
from plugins.snakes import Snakes
from plugins.snakes2 import Snakes as Snakes2
from plugins.ec import EC
from plugins.fancyrainbow import FancyRainbow
from plugins.sometext import SomeText

curtain = Curtain()

#plugins = [FancyRainbow(), EC(), Strobe()]
#plugins = [EC()]
#plugins = [Snakes()]
plugins = [Snakes2(), EC(), FancyRainbow()]


def weighted_average(a, b, f):
    average = {}
    for k in set(a.keys() + b.keys()):
        r1, g1, b1 = a.get(k, (0, 0, 0))
        r2, g2, b2 = b.get(k, (0, 0, 0))
        average[k] = (f*r1 + (1-f)*r2, f*g1 + (1-f)*g2, f*b1 + (1-f)*b2)
    return average


frame = 0
while True:
    frame_start = time.clock()

    frame += 1

    for plugin in plugins:
        plugin.step()

    plugin = plugins[(int(frame / 600) + 2) % len(plugins)]

    curtain.send_color_dict(plugin.canvas)

    frame_end = time.clock()
    sleep_length = frame_length - (frame_end - frame_start)
    time.sleep(sleep_length)
