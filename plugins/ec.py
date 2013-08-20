from curtain import width, height, brightness
from plugin import Plugin
from colorsys import hsv_to_rgb
from letters import letters
import math, time, random

class EC(Plugin):
    def __init__(self):
        super(EC, self).__init__()

        self.n = 0
        self.d = True
        self.text = ['E', 'bolt', 'C']

    def draw(self):
        h = math.fmod(self.time, 2)
        if h >= 1:
            h = 2 - h

        x = int(round(self.n))
        offset = 1.0 / (len(self.text) + 1)

        r, g, b = hsv_to_rgb(h, 1, 0.03)
        self.canvas.clear(r, g, b)

        h = math.fmod(h + offset, 1)

        length = -1
        for c in self.text:
            length += letters[c].width + 1

        x = (width - length + 1) / 2

        for c in self.text:
            r, g, b = hsv_to_rgb(h, 1, brightness)
            h = math.fmod(h + offset, 1)

            letter = letters[c]
            self.canvas.add_letter(letter, x, 0, r, g, b)
            x += letter.width + 1

        if self.n > 15 or self.n < -15:
            self.d = not self.d
            #if self.d:
                #self.text = ['4','E']
                #self.n += .3
                #else:
        #self.text = ['E', 'bolt', 'C']
            #self.n -= .3

