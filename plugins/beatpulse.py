from curtain import width, height, brightness
from letters import letters
from plugin import Plugin
from colorsys import hsv_to_rgb
import math, time, random
from math import sin
from beat_sender import beat_event_pb2


class BeatPulse(Plugin):
    def __init__(self):
        super(BeatPulse, self).__init__()
        self.fading_number = 0
        self.hue = 0

    def draw(self):
        self.fading_number -= 0.03
        self.fading_number = max(0, self.fading_number)
        # self.hue += 0.001

        # self.canvas.clear(
        #     *hsv_to_rgb(
        #         self.hue,
        #         1.0,
        #         self.fading_number
        #     )
        # )

        for x in xrange(width):
            for y in xrange(height):
                self.canvas.draw_pixel(
                    x, y,
                    *hsv_to_rgb(self.hue, 1, self.fading_number * (height - y) / float(height))
                )

    def recv_beat(self, beat_event):
        if beat_event.type == beat_event_pb2.BEAT:
            self.hue += 0.1
            self.hue = self.hue % 1
            self.fading_number = 1
