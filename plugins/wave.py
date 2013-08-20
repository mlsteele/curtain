from curtain import width, height, brightness
from letters import letters
from plugin import Plugin
from colorsys import hsv_to_rgb
import math, time, random
from math import sin


class Wave(Plugin):
    def __init__(self):
        super(Wave, self).__init__()

    def draw(self):
        for x in xrange(width):
            for y in xrange(height):
                def like_sin(n):
                    """ Will always return between 0 and 1. """
                    return (sin(n) + 1) / 4.

                self.canvas.draw_pixel(
                    x, y,
                    *hsv_to_rgb(
                        like_sin(self.time + sin(x + self.time) + sin(y)),
                        1,
                        1,
                    )
                )
