import pygame
import sys
import config
from curtain import width, height


# Coordinates of broken pixels on the curtain.
BROKEN_PIXELS_ALL = [(0, 4), (1,4), (2,4), (14,4), (13,4), (12,4)]
BROKEN_PIXELS_RED = [(5, 1), (9, 1)]
BROKEN_PIXELS_GREEN = [(2, 1), (1, 2), (9, 1), (12, 3)]
BROKEN_PIXELS_BLUE = []


class Cell(object):
    def __init__(self, position, size, padding):
        self.position = position
        self.size = size
        self.padding = padding
        self.rect = pygame.Rect((
            self.position[0] * self.size,
            self.position[1] * self.size,
            ),(
            self.size - self.padding,
            self.size - self.padding,
        ))
        self.color = 150, 0, 0
    def set_color(self, r, g, b):
        map_color = r, g, b
        if self.position in broken_red: map_color[0] = 0
        if self.position in broken_green: map_color[1] = 0
        if self.position in broken_blue: map_color[2] = 0
        self.color = map_color


class PygameCurtain(object):
    def __init__(self):
        # measurements in cells
        self.size_cells = width, height

        # measurements in pixels
        self.cell_scale = 60
        self.cell_padding = 10
        self.size_px = self.size_cells[0] * self.cell_scale, self.size_cells[1] * self.cell_scale

        self.screen = pygame.display.set_mode(self.size_px)

        # initialize grid of cells
        self.cells = [[
            Cell((x,y), size=self.cell_scale, padding=self.cell_padding)
            for y in xrange(self.size_cells[1])]
            for x in xrange(self.size_cells[0])
        ]

        self._render_cells()

    def _render_cells(self):
        for x in xrange(width):
            for y in xrange(height):
                cell = self.cells[x][y]
                if not config.RENDER_FAULTS:
                    pygame.draw.rect(self.screen, cell.color, cell.rect)
                else:
                    if (x, y) not in BROKEN_PIXELS_ALL:
                        pygame.draw.rect(self.screen, cell.color, cell.rect)

    def send_color_dict(self, color_dict):
        """
        Render the `color_dict`.

        `color_dict` is a dict where the keys are tuples
        in the bounds of `width` and `height` and the values
        are tuples of r, g, b.
        """
        # for (x, y), (r, g, b) in color_dict:
        #     print x, y, r, g, b
        # for foo in color_dict.items():
        #     print foo
        #     print type(foo)
        for (x, y), (r, g, b) in color_dict.items():
            self.cells[x][y].color = r * 255, g * 255, b * 255

        self._render_cells()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
