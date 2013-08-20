from curtain import width, height
from plugin import Plugin
from colorsys import hsv_to_rgb
import math

class Rainbow(Plugin):
    def __init__(self):
        super(Rainbow, self).__init__()

    def draw(self):
        h = math.fmod(self.time * 1, 2)
        if h >= 1:
            h = 2 - h

        i = 0.3 * (math.fmod(self.time, 0.8) + 0.2)

        r, g, b = hsv_to_rgb(h, 1, i)

        self.canvas.clear(r, g, b)


