from curtain import width, height, brightness
from letters import letters
from plugin import Plugin
from colorsys import hsv_to_rgb
import math, time, random


class Conway(Plugin):
    def __init__(self):
        super(Conway, self).__init__()

        self.grid = LifeGrid(width, height).randomized()
        # for x in xrange(width):
        #     for y in xrange(height):
        #         # self.grid.cells[x][y] = x % 2 or y % 2
        #         self.grid.cells[x][y] = random.choice([0, 1])
        # self.grid.cells[0][1] = 1
        # self.grid.cells[1][1] = 1
        # self.grid.cells[2][1] = 1
        # self.grid.cells[3][1] = 1
        # self.grid.cells[4][1] = 1

    def draw(self):
        self.canvas.clear(*hsv_to_rgb(0, 0, 0))

        if self.frame % 4 is 0:
            if self.grid.is_empty():
                self.grid = self.grid.randomized()
            else:
                self.grid = self.grid.next()

        # render snakes
        for x in range(width):
            for y in range(height):
                val = self.grid.cells[x][y]
                brightness = val * 0.5
                self.canvas.draw_pixel(x, y, *hsv_to_rgb(
                    0, 0, brightness
                ))


class LifeGrid(object):
    """
    State of game of life.

    Any live cell with fewer than two live neighbours dies, as if caused by under-population.
    Any live cell with two or three live neighbours lives on to the next generation.
    Any live cell with more than three live neighbours dies, as if by overcrowding.
    Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = [[0 for _ in xrange(height)] for _ in xrange(width)]

    def neighbors(self, x, y):
        deltas = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
        for dx, dy in deltas:
            nx, ny = x + dx, y + dy
            if 0 < nx < self.width and 0 < ny < self.height:
                yield nx, ny

    def next(self):
        """ Generate the next state. """
        next = LifeGrid(self.width, self.height)
        for x in xrange(self.width):
            for y in xrange(self.height):
                live_neighbors = sum(self.cells[nx][ny] for nx, ny in self.neighbors(x, y))
                # HACK all the constants have been tweaked to be wrong.
                if self.cells[x][y] is 1:
                    if live_neighbors < 1 or live_neighbors > 2:
                        next.cells[x][y] = 0
                else:
                    if live_neighbors is 2:
                        next.cells[x][y] = 1
        return next

    def randomized(self):
        next = LifeGrid(self.width, self.height)
        for x in xrange(self.width):
            for y in xrange(self.height):
                next.cells[x][y] = random.choice([0, 1])
        return next

    def is_empty(self):
        return sum(sum(column) for column in self.cells) is 0
