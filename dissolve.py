from curtain import Curtain, Canvas, width, height
from letters import letters
from colorsys import hsv_to_rgb
import math, time, random

curtain = Curtain()
canvas = Canvas()

now = 0.0
time_step = 0.033

text = ["E", "bolt", "C"]

canvas.clear(0, 0, 1.0 / 255.0)

x = 2

offset = 1.0 / len(text)

h = random.random()

for c in text:
    r, g, b = hsv_to_rgb(h, 1, 0.08)
    h = math.fmod(h + offset, 1)

    letter = letters[c]
    canvas.draw_letter(letter, x, 0, r, g, b)
    x += letter.width + 1

def do_frame():
    h = math.fmod(now, 2)
    if h >= 1:
        h = 2 - h

    canvas.draw_pixel(random.randint(0, width - 1), random.randint(0, height - 1), 0, 0, 1.0 / 255.0)

while True:
    do_frame()
    curtain.send_color_dict(canvas)
    now += time_step
    time.sleep(time_step)

