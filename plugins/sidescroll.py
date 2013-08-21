from curtain import width, height, brightness
from plugin import FinitePlugin
from colorsys import hsv_to_rgb
from letters import letters
from string import split
import math, time, random


class SideScroll(FinitePlugin):
    def __init__(self, text="SCROLLING TEXT"):
        super(SideScroll, self).__init__()
        self.sst = SideScrollText(list(text))

    def draw(self):
        self.canvas.clear(*hsv_to_rgb(0, 0, 0))
        self.sst.draw(self.canvas)
        self.sst.step(0.5)
        if self.sst.is_done:
            self.is_done = True


class SideScrollText(object):
    def __init__(self, text):
        """ Text is an array of letter names. """
        self.text = text
        self.letters = [letters[c] for c in self.text]
        self.width = sum(let.width + 1 for let in self.letters)
        self._offset = width
        self.is_done = False

    def step(self, delta=1):
        """ Step one pixel to the left. """
        self._offset -= delta
        if self._offset < -self.width:
            self.is_done = True

    def draw(self, canvas, r=1, g=0, b=0):
        x = int(self._offset)
        for let in self.letters:
            canvas.add_letter(let, x, 0, r, g, b)
            x += let.width + 1


def SideScrollCreator(text):
    def fake_custom_constructor():
        return SideScroll(text=text)
    return fake_custom_constructor
