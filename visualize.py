import pyaudio
import struct
from numpy.fft import fft
from numpy import average
from math import floor, ceil
from curtain import Curtain, Canvas
from random import random
from colorsys import hsv_to_rgb
import sys
import random

# Colors are a rotation over HSV
def generate_colors():
    colors = []
    for x in range(0, 15):
        # H: 0.9 -> 0.5, a purple -> blue gradient
        print 0.5+((15-x)/15.0*0.4)
        r, g, b = hsv_to_rgb(0.5+((15-x)/15.0*0.4), 1, .3)
        colors += [(r, g, b)]
    return colors

# The array of values should be length-15, each 0-5 representing the
# amount of bar to draw in that column
def draw_music(canvas, colors, values):
    x = 0
    for v in values:
        r, g, b = colors[x]
        for y in range(5 - int(v), 5):
            canvas.draw_pixel(x, y, r, g, b)
        x += 1
        
if __name__ == '__main__':
    
    chunk = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 1
    
    p = pyaudio.PyAudio()
    stream = p.open(format = FORMAT,
				    channels = CHANNELS,
				    rate = RATE,
				    input = True,
				    frames_per_buffer = chunk)
    
    curtain = Curtain()
    canvas = Canvas()
    colors = generate_colors()
    while 1:
        canvas.clear(0, 0, 0)
        draw_music(canvas, colors, [random.choice([0,1,2,3,4,5]) for i in range(15)])
        curtain.send_color_dict(canvas)
        
        values = []
        data = ''.join(stream.read(chunk))
        samples = abs(fft(list(struct.unpack("%dh" % chunk, data))))
        lx = 14
        for x in range(28, 228, 14):
            values += [abs(sum(samples[lx:x])/(lx-x))]
            lx = x
        values[0] = abs(average(samples[2:4]))
        mx = max(values)
    	values = [round(v / mx * 5.0) for v in values]
    	print values
    sys.exit()
