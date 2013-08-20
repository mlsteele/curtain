from curtain import width, height, brightness
from letters import letters
from plugin import Plugin
from colorsys import hsv_to_rgb
import math, time, random

class Snake(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.dx = 1
        self.dy = 0
        self.data = [[-100000] * height for x in range(width)]
        self.time = 0

    def step(self):
        if random.random() > 0.6:
            flip = random.choice([-1, +1])
            self.dx, self.dy = self.dy * flip, self.dx * flip

        self.x = (self.x + self.dx + width) % width
        self.y = (self.y + self.dy + height) % height

        self.data[self.x][self.y] = self.time
        self.time += 1

class Snakes(Plugin):
    def __init__(self):
        super(Snakes, self).__init__()
        
        self.snakes = [Snake() for i in range(20)]

    def draw(self):
        h = math.fmod(self.time / 2, 2)

        if h >= 1:
            h = 2 - h

        self.canvas.clear(0, 0, 1.0 / 255.0)

        if self.frame % 2 == 0:
            for snake in self.snakes:
                snake.step()

        for snake in self.snakes:
            h = math.fmod(h + 1.0 / len(self.snakes), 1)
            for x in range(width):
                for y in range(height):
                    v = max(0, float(snake.data[x][y] - snake.time + 20.0) / 20.0)
                    v = min(brightness, v**2 * brightness * 4)
                    if v > 0.01:
                        r, g, b = hsv_to_rgb(h, 1, v)
                        self.canvas.draw_pixel(x, y, r, g, b)
