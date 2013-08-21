import time
from curtain import frame_length


class SlideShow(object):
    """ Rotating list of plugins. """
    def __init__(self, period):
        """
        `period` is in seconds.
        """
        self.period = period
        self.plugins = []
        self.active_plugin = None
        # timer for each slide
        self.timer = None

    def add(self, plugin_constructor):
        """ `plugin_constructor` is the plugin class. """
        self.plugins.append(plugin_constructor)

    def step(self):
        # initialize active_plugin
        if self.active_plugin is None:
            self.active_plugin = self.plugins[0]()

        # one-time intiialize timer
        if self.timer is None:
            self.timer = time.time()

        # rotate when out of time (even if finite plugin)
        if time.time() > self.timer + self.period:
            self.rotate()

        # rotate finite plugins
        if hasattr(self.active_plugin, 'is_done') and self.active_plugin.is_done:
            self.rotate()

        self.active_plugin.step()

    def rotate(self):
        print "rotating slideshow to {}".format(self.active_plugin.__class__.__name__)
        self.plugins = self.plugins[1:] + [self.plugins[0]]
        self.active_plugin = self.plugins[0]()
        self.timer = time.time()


class ViewManager(object):
    def __init__(self, curtain, bg):
        """
        `bg` is a SlideShow of plugins to run in the background.
        """
        self.curtain = curtain
        self.bg = bg

    def start(self):
        """ Start the render loop. (blocking) """
        frame = 0
        while True:
            frame_start = time.clock()
            frame += 1
            self.bg.step()
            self.curtain.send_color_dict(self.bg.active_plugin.canvas)
            frame_end = time.clock()
            sleep_length = frame_length - (frame_end - frame_start)
            time.sleep(sleep_length)
