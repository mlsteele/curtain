from curtain import Curtain, frame_length
from plugin import Plugin
import time, os, math

plugins = []

for filename in os.listdir('plugins'):
    name, extension = os.path.splitext(filename)
    if extension == '.py' and name != '__init__':
        module = __import__('plugins.' + name).__dict__[name]

        for var in module.__dict__.values():
            if isinstance(var, type) and Plugin in var.__bases__:
                plugins.append(var)

        
curtain = Curtain()
from plugins.strobe import Strobe
from plugins.rainbow import Rainbow
from plugins.snakes import Snakes
from plugins.ec import EC
from plugins.fancyrainbow import FancyRainbow
plugins = [FancyRainbow(), EC(), Strobe()]

def weighted_average(a, b, f):
    average = {}
    for k in set(a.keys() + b.keys()):
        r1, g1, b1 = a.get(k, (0, 0, 0))
        r2, g2, b2 = b.get(k, (0, 0, 0))
        average[k] = (f*r1 + (1-f)*r2, f*g1 + (1-f)*g2, f*b1 + (1-f)*b2)
    return average

frame = 0

while True:
    start = time.clock()

    frame += 1

    for plugin in plugins:
        plugin.step()

    plugin = plugins[(int(frame / 600) + 2) % len(plugins)]

    curtain.send_color_dict(plugin.canvas)

    end = time.clock()
    sleep_length = frame_length - (end - start)
    if sleep_length > 0:
        time.sleep(sleep_length)

