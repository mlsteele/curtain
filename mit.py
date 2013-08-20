from curtain import Curtain, Canvas
from letters import letters
from colorsys import hsv_to_rgb
import math, time

curtain = Curtain()
canvas = Canvas()

now = 0.0
time_step = 0.033

text = ["M", "I", "T"]

n = 0
d = True
def do_frame():
    global n
    global d
    global text
    h = math.fmod(now, 2)
    if h >= 1:
        h = 2 - h
    almost_nil = 1.0 / 255.0
    canvas.clear(0, 0, almost_nil)
    x = int(round(n))
    offset = 1.0 / len(text)

    for c in text:
        r, g, b = hsv_to_rgb(h, 1, 0.4)
        h = math.fmod(h + offset, 1)

        letter = letters[c]
        canvas.draw_letter(letter, x, 0, r, g, b)
	x += letter.width + 1
    #canvas.draw_pixel(3, 0, r, g, b)
    if n > 15 or n < -15:
        d = not d
    if d:
        text = ['E', 'bolt', 'C']
	n += .3
    else:
        text = ['E', 'bolt', 'C']
        n -= .3
while True:
    do_frame()
    curtain.send_color_dict(canvas)
    now += time_step
    time.sleep(time_step)

