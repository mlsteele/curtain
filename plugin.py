from curtain import Canvas
import time

class Plugin(object):
    """
    A visualization.

    Has a `canvas`, `time`, and `frame`.
    """
    def __init__(self):
        self.canvas = Canvas()
        self._start_time = time.time()
        self.frame = 0

    @property
    def time(self):
        return time.time() - self._start_time

    def step(self):
        self.frame += 1
        self.draw()

    def draw(self):
        raise NotImplementedError("plugin must override draw()")


class FinitePlugin(Plugin):
    """ A plugin which can be finished. """
    def __init__(self):
        super(FinitePlugin, self).__init__()
        self.is_done = False

    def step(self):
        if self.is_done:
            print "WARN: FinitePlugin stepping after done."
        super(FinitePlugin, self).step()
