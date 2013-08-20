import pygame
import sys
from curtain import width, height


class Cell(object):
    def __init__(self, position, size):
        self.position = position
        self.size = size
        self.rect = pygame.Rect((
            self.position[0] * self.size,
            self.position[1] * self.size
            ),(
            self.size,
            self.size
        ))
        self.color = 150, 0, 0


class PygameCurtain(object):
    def __init__(self):
        # measurements in cells
        self.size_cells = width, height

        # measurements in pixels
        self.cell_scale = 60
        self.size_px = self.size_cells[0] * self.cell_scale, self.size_cells[1] * self.cell_scale

        self.screen = pygame.display.set_mode(self.size_px)

        # initialize grid of cells
        self.cells = [[Cell((x,y), self.cell_scale) for y in xrange(self.size_cells[1])] for x in xrange(self.size_cells[0])]

        self._render_cells()

    def _render_cells(self):
        for column in self.cells:
            for cell in column:
                cell.rect
                cell.color
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
