from curtain import width, height, brightness
from plugin import Plugin
from colorsys import hsv_to_rgb
import math
import time
import random

class HeightLines(Plugin):
    def __init__(self):
        super(HeightLines, self).__init__()
        self.heights = [height - 1] * width
        self.heights[2] = 0

    def draw(self):
        # change heights
        heights = [x for x in self.heights]
        for x in xrange(width):
            if random.random() > 0.3:
                delta = random.choice([-1, 0, 1])
                heights[x] += delta

            # tend towards neighbors
            if x > 0:
                if random.random() > 0.8:
                    delta = (self.heights[x-1] - self.heights[x])
                    delta = max(-1, min(delta, 1))
                    heights[x] += delta
            if x < width - 1:
                if random.random() > 0.8:
                    delta = (self.heights[x+1] - self.heights[x])
                    delta = max(-1, min(delta, 1))
                    heights[x] += delta

            # stay in bounds of height
            heights[x] = max(0, min(heights[x], height))
        self.heights = heights
        # print heights

        # render
        self.canvas.clear(*hsv_to_rgb(0, 0, 0))
        for x in xrange(width):
            for y in xrange(height):
                if y < self.heights[x]:
                    self.canvas.draw_pixel(x, y, *hsv_to_rgb(
                        0.65, 1, 0.02
                    ))
                else:
                    self.canvas.draw_pixel(x, y, *hsv_to_rgb(
                        random.choice([0.1, 0.05]), 1, 0.4
                    ))
