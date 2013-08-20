from curtain import Canvas, frame_length

class Plugin(object):
    def __init__(self):
        self.canvas = Canvas()

        self.time = 0.0
        self.frame = 0

    def step(self):
        self.time += frame_length
        self.frame += 1
        self.draw()

    def draw(self):
        raise NotImplementedError("plugin must override draw()")
