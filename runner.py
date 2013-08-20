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
from plugins.sidescroll import SideScroll
from plugins.wave import Wave

curtain = Curtain()


# plugins = [FancyRainbow, EC, Strobe]
# plugins = [EC]
# plugins = [Snakes2]
# plugins = [Snakes2, EC, FancyRainbow]
# plugins = [SideScroll]
# plugins = [Wave]
plugins = [SideScroll, Wave, Snakes2, FancyRainbow]
# plugin rotation period in seconds
plugin_period = 10
active_plugin = plugins[0]()


def rotate_plugins():
    print "rotating plugins"
    global plugins
    global active_plugin
    plugins = [plugins.pop()] + plugins
    active_plugin = plugins[0]()


frame = 0
plugin_start = time.time()
while True:
    frame_start = time.clock()
    frame += 1
    if time.time() > plugin_start + plugin_period:
        rotate_plugins()
        plugin_start = time.time()
    active_plugin.step()
    curtain.send_color_dict(active_plugin.canvas)
    frame_end = time.clock()
    sleep_length = frame_length - (frame_end - frame_start)
    time.sleep(sleep_length)
