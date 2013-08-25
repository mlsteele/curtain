from curtain import width, height
from plugin import Plugin
from colorsys import hsv_to_rgb
import math

class ColorTest(Plugin):
    def __init__(self):
        super(ColorTest, self).__init__()

    def draw(self):
        if (self.frame / 100) % 3 == 0:
            self.canvas.clear(1, 0, 0)
        if (self.frame / 100) % 3 == 1:
            self.canvas.clear(0, 1, 0)
        if (self.frame / 100) % 3 == 2:
            self.canvas.clear(0, 0, 1)
