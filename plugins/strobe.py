from curtain import width, height
from plugin import Plugin
from colorsys import hsv_to_rgb
import math

class Strobe(Plugin):
    def __init__(self):
        super(Strobe, self).__init__()
	self.period = 6

    def draw(self):
        h = math.fmod(self.time * 2, 2)
        if h >= 1:
            h = 2 - h

        i = 0.5 if self.frame % self.period == 0 else 0
        #if self.frame % 5 == 1:
            #i = 0.05

        r, g, b = hsv_to_rgb(h, 1, i)

        self.canvas.clear(r, g, b)

