from curtain import width, height, brightness
from plugin import Plugin
from colorsys import hsv_to_rgb
import math
import time

class FancyRainbow(Plugin):
    hue = 0.5
    def __init__(self):
        super(FancyRainbow, self).__init__()

    def draw(self):
        self.hue += 0.005
        self.hue = self.hue % 360
        r, g, b = hsv_to_rgb(self.hue, 1, 1)
        self.canvas.clear(r, g, b)
