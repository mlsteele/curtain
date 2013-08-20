from curtain import Curtain, Canvas, width, height
from letters import letters
from colorsys import hsv_to_rgb
import math, time, random

curtain = Curtain()
canvas = Canvas()

now = 0.0
time_step = 0.04

while True:
    h = math.fmod(now * 5, 2)
    if h >= 1:
        h = 2 - h

    if math.fmod(now, .08) > .04:
        i = 1
    else:
        i = 0

    r, g, b = hsv_to_rgb(h, 1, i)

    canvas.clear(r, g, b)
    print (r, g, b)
    curtain.send_color_dict(canvas)
    now += time_step
    time.sleep(time_step)

