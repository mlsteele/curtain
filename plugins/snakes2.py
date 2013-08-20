from curtain import width, height, brightness
from letters import letters
from plugin import Plugin
from colorsys import hsv_to_rgb
import math, time, random

class BSSnake(object):
    """ Data container for a snake's position. """
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

class Snake(object):
    def __init__(self, length=7):
        self.pos = [int(random.random() * width), int(random.random() * height)]
        self.length = length
        self.grid = [[0 for _ in range(height)] for _ in range(width)]
        self.color = random.choice([0, 0.12, 0.38, 0.60, 0.75])

        self.grid[self.pos[0]][self.pos[1]] = self.length

    def step(self):
        self._fade()

        # move random direction
        deltas = [[-1,0], [0,-1], [1,0], [0,1]]
        delta = random.choice(deltas)
        self.pos[0] += delta[0]
        self.pos[1] += delta[1]

        # stay in bounds
        self.pos[0] = max(0, min(self.pos[0], width - 1))
        self.pos[1] = max(0, min(self.pos[1], height - 1))

        # update grid
        self.grid[self.pos[0]][self.pos[1]] = self.length

    def _fade(self):
        for x in range(width):
            for y in range(height):
                self.grid[x][y] = max(0, self.grid[x][y] - 1)


class Snakes(Plugin):
    def __init__(self):
        super(Snakes, self).__init__()

        n_snakes = 4
        self.snakes = [Snake() for _ in range(n_snakes)]

    def draw(self):
        if random.random() > 0.95:
            self.snakes.pop()
            self.snakes.append(Snake(length=random.randint(1, 14)))

        self.canvas.clear(*hsv_to_rgb(0, 0, 0))

        # setp all snakes
        for snake in self.snakes:
            snake.step()

        # render snakes
        for snake in self.snakes:
            for x in range(width):
                for y in range(height):
                    val = snake.grid[x][y]
                    if val > 0:
                        self.canvas.draw_pixel(x, y, *hsv_to_rgb(
                            snake.color, 1, float(val) / snake.length
                        ))
