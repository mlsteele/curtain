from curtain import width, height, brightness
from letters import letters
from plugin import Plugin
from colorsys import hsv_to_rgb
import math, time, random
from math import sin


class BeatPulse(Plugin):
    def __init__(self):
        super(BeatPulse, self).__init__()
        self.fading_number = 0

    def draw(self):
        self.fading_number -= 0.05
        self.fading_number = max(0, self.fading_number)

        self.canvas.clear(
            *hsv_to_rgb(
                0.25,
                self.fading_number,
                1,
            )
        )

    def recv_beat(self, beat_event):
        print beat_event
        self.fading_number = 1
