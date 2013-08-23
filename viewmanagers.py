import time
from curtain import frame_length
import config

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
    """
    Handle displaying of plugins.

    Control methods (like `interrupt`) must be called from a seperate thread
    as `start()` blocks the main thread.
    """
    def __init__(self, curtain, bg):
        """
        `bg` is a `SlideShow` of plugins to run in the background.
        """
        self.curtain = curtain
        self.bg = bg
        # False to watch background slidedshow.
        self.active_plugin = None

    def start(self):
        """ Start the render loop. (blocking) """
        print "ViewManager started"
        frame = 0
        while True:
            frame_start = time.clock()
            frame += 1
            if self.can_run():
                if self.active_plugin is None:
                    self.bg.step()
                    self.curtain.send_color_dict(self.bg.active_plugin.canvas)
                else:
                    if self.active_plugin.is_done:
                        self.active_plugin = None
                    else:
                        self.active_plugin.step()
                        self.curtain.send_color_dict(self.active_plugin.canvas)
            frame_end = time.clock()
            sleep_length = frame_length - (frame_end - frame_start)
            time.sleep(sleep_length)

    def rotate_bg(self):
        """ Skip to the next plugin in the bg slideshow. """
        self.bg.rotate()

    def interrupt(self, plugin_constructor):
        """
        Interrupt the background slideshow with a high priority plugin.

        `plugin_constructor` is the plugin class.
        """
        print "ViewManager interrupted."
        self.active_plugin = plugin_constructor()
        if not hasattr(self.active_plugin, 'is_done'):
            raise ValueError("Interrupt plugin must have an is_done property.")

    def recv_beat(self, beat_event):
        if self.active_plugin is None:
            if hasattr(self.bg.active_plugin, 'recv_beat'):
                self.bg.active_plugin.recv_beat(beat_event)
        else:
            if hasattr(self.active_plugin, 'recv_beat'):
                self.active_plugin.recv_beat(beat_event)

    def can_run(self):
        """
        Decides whether the curtain is allowed to run.
        For now, just takes into account quiet hours (in config.py)
        """
        if config.ENABLE_QUIET_HOURS:
            current_time = int(time.strftime("%H%M"))
            if config.QUIET_HOURS_START > config.QUIET_HOURS_END:
                #Quiet hours include midnight
                if current_time >= config.QUIET_HOURS_START or current_time <= config.QUIET_HOURS_END:
                    print "In quiet hours!"
                    return False
            else:
                #Quiet hours don't include midnight
                if current_time >= config.QUIET_HOURS_END and current_time <= config.QUIET_HOURS_END:
                    print "In quiet hours!"
                    return False
        print "Not in quiet hours! Quiet hours are from", config.QUIET_HOURS_START, "to", config.QUIET_HOURS_END
        print "Now is", current_time
        return True