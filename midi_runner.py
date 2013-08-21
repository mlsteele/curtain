from curtain import Curtain, frame_length
import sys
from plugin import Plugin
import time, os, math

import midi
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
plugins = [Strobe(),Snakes(), FancyRainbow(), EC(),Strobe()]
input = midi.MidiInput(9)
class Constants():
    p = 3
def do_strobe(lol):
    print "strobe"
    Constants.p = 0
def do_strobe_2(lol):
    print "strobe"
    Constants.p = 4
def do_rainbow(lol):
    global p
    Constants.p=2
def do_snakes(lol):
    global p
    Constants.p=1
def do_ec(lol):
    global p
    Constants.p = 3
def set_period(rate):
    rate = int((127*3)/(rate+1))
    plugins[0].period = rate

def set_period_2(rate):
    rate = int((127*3)/(rate+1))
    plugins[4].period = rate/5+2
input.attach_callback(102,do_strobe)
input.attach_callback(106,do_strobe_2)
input.attach_callback(103,do_rainbow)
input.attach_callback(104,do_snakes)
input.attach_callback(105,do_ec)
input.attach_callback(16,set_period)
input.attach_callback(20,set_period_2)
input.start()
def weighted_average(a, b, f):
    average = {}
    for k in set(a.keys() + b.keys()):
        r1, g1, b1 = a.get(k, (0, 0, 0))
        r2, g2, b2 = b.get(k, (0, 0, 0))
        average[k] = (f*r1 + (1-f)*r2, f*g1 + (1-f)*g2, f*b1 + (1-f)*b2)
    return average

frame = 0
try:
    while True:
        start = time.clock()

        frame += 1

        for plugin in plugins:
            plugin.step()

        plugin =plugins[Constants.p] # plugins[(int(frame / 600) + 2) % len(plugins)]

        curtain.send_color_dict(plugin.canvas)

        end = time.clock()
        sleep_length = frame_length - (end - start)
        if sleep_length > 0:
            time.sleep(sleep_length)
except Exception:
    input.stop()
    sys.exit(0)
