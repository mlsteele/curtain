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


class SlideShow(object):
    def __init__(self, period):
        """
        `period` is in seconds.
        """
        self.period = period
        self.plugins = []
        self.active_plugin = None
        self.timer = None

    def add(self, plugin):
        self.plugins.append(plugin)

    def step(self):
        if self.active_plugin is None:
            self.active_plugin = self.plugins[0]()

        if self.timer is None:
            self.timer = time.time()

        if time.time() > self.timer + self.period:
            self.rotate()

        self.active_plugin.step()

    def rotate(self):
        print "rotating slideshow to {}".format(self.active_plugin.__class__.__name__)
        self.plugins = self.plugins[1:] + [self.plugins[0]]
        self.active_plugin = self.plugins[0]()
        self.timer = time.time()


slideshow = SlideShow(period=15)
slideshow.add(FancyRainbow)
slideshow.add(EC)
slideshow.add(Snakes2)
slideshow.add(Wave)
slideshow.add(Strobe)
slideshow.add(SideScroll)

frame = 0
while True:
    frame_start = time.clock()
    frame += 1
    slideshow.step()
    curtain.send_color_dict(slideshow.active_plugin.canvas)
    frame_end = time.clock()
    sleep_length = frame_length - (frame_end - frame_start)
    time.sleep(sleep_length)
