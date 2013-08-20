from curtain import width, height

class Cell(object):
    def __init__(self, position):
        self.position = position
        self.rect = pygame.Rect((self.position[0]*self.cell_size, self.position[1]*self.cell_size), (self.cell_size, self.cell_size))
        self.color = 0, 0, 0

class PygameCurtain(object):
    def __init__(self):
        self.width = width
        self.height = height
        self.cell_size = 20
        self.psize = self.pwidth, self.pheight = self.width*self.cell_size, self.height*self.cell_size #in pixels

        self.screen = pygame.display.set_mode(self.psize)

        #Initialize cells
        self.cells = []
        for top in range(0, self.pheight/self.cell_size):
            cellrow = []
            for left in range(0, self.pwidth/self.cell_size):
                cell = Cell((left, top))
                # cell.alive = bool(random.randrange(100)>75) #randomize livelihood
                cellrow.append(cell)
            self.cells.append(cellrow)

    def send_color_dict(self, color_dict):
        """
        Render the `color_dict`.

        `color_dict` is a dict where the keys are tuples
        in the bounds of `width` and `height` and the values
        are tuples of r, g, b.
        """
        raise NotImplementedError()
