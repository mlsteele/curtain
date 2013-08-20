from curtain import width, height, brightness
from plugin import Plugin
from colorsys import hsv_to_rgb
from letters import letters
import math, time, random

class SideScroll(Plugin):
    def __init__(self):
        super(SideScroll, self).__init__()
        self.text = "NO SHOES NO BURGERS!"
        self.text.split()
        self.offset_x = 10

    def draw(self):
        self.canvas.clear(*hsv_to_rgb(0, 0, 0))

        x = int(self.offset_x)
        for c in self.text:
            self.canvas.add_letter(letters[c], x, 0, *hsv_to_rgb(0, 0.5, 0.5))
            x += letters[c].width + 1

        self.offset_x -= 0.5
