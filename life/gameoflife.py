from curtain import Curtain, Canvas, width, height
from letters import letters
from colorsys import hsv_to_rgb
import math, time, random

curtain = Curtain()
canvas = Canvas()

intensity = [[1.0] * height for x in range(width)]

def draw_on_curtain(life, seconds):
    h = math.fmod(seconds * 0.2, 2)
    if h >= 1:
        h = 2 - h

    r, g, b = hsv_to_rgb(h, 1, 0.3)

    canvas.clear(0, 0, 1.0 / 255.0)

    for x in range(width):
        for y in range(height):
            if life[x+1][y+1] == 1:
                intensity[x][y] = min(intensity[x][y] + 0.01, .1)
            else:
                intensity[x][y] *= .7
            r, g, b = hsv_to_rgb(h, 1, intensity[x][y])
            canvas.draw_pixel(x, y, r, g, max(b, 1.0 / 255.0))

    curtain.send_color_grid(canvas.color_grid)

    
import pygame
import random
xsize = 17
ysize = 7
k=20
life1 = [[0 for i in range(0,ysize)] for j in range(0,xsize)]
life2 = [[0 for i in range(0,ysize)] for j in range(0,xsize)]

for y in range (1,ysize-1):
    for x in range (1,xsize-1):
        if random.randint(0,100)<15:
            life1[x][y]=1

def drawpixel((x,y),(a,b,c)):
    global k
    for i in range (0,k):
        for j in range (0,k):
            screen.set_at(((x-1)*k+i,(y-1)*k+j),(a,b,c))

def live():
    global life1
    global life2
    global play
    global grid
    if play == 1:
        for y in range (1,ysize-1):
            for x in range (1,xsize-1):
                neighbors = life1[x-1][y-1]+life1[x][y-1]+life1[x+1][y-1]+life1[x-1][y]+life1[x+1][y]+life1[x-1][y+1]+life1[x][y+1]+life1[x+1][y+1]
                if life1[x][y]==1:
                    #drawpixel((x,y),(255,0,0))
                    if neighbors < 2:
                        life2[x][y]=0
                    if neighbors > 3:
                        life2[x][y]=0
                    if neighbors == 2:
                        life2[x][y]=1
                    if neighbors == 3:
                        life2[x][y]=1
                else:
                    #drawpixel((x,y),(0,0,0))
                    if neighbors == 3:
                        life2[x][y]=1
                    else:
                        life2[x][y]=0
                        
        for y in range (1,ysize-1):
            for x in range (1, xsize-1):
                life1[x][y]=life2[x][y]
                drawpixel((x,y),(255*life1[x][y],0,0))

def switch((x,y)):
    global life1
    global life2
    x=x+k
    y=y+k
    life1[x/k][y/k]=(life1[x/k][y/k]+1)%2

def draw((x,y)):
    x=x+k
    y=y+k
    if life1[x/k][y/k]==1:
        drawpixel((x/k,y/k),(255,0,0))
    if life1[x/k][y/k]==0:
        drawpixel((x/k,y/k),(0,0,0))
        
def drawgrid(a,b,c):
    for y in range (1,ysize-2):
        for x in range (1,(xsize-2)*k):
            screen.set_at((x,y*k),(a,b,c))
    for x in range (1,xsize-2):
        for y in range (1,(ysize-2)*k):
            screen.set_at((x*k,y),(a,b,c))

clock = pygame.time.Clock()
running = True
play = 1
grid = 1
screen = pygame.display.set_mode((k*(xsize-2),k*(ysize-2)))

since_last_tick = 0
tick_length = 0.5

while running:
    since_last_tick += clock.get_time() / 1000.0
    if since_last_tick >= tick_length:
        live()
        since_last_tick = 0.0
    if grid == 1:
        drawgrid(100,100,100)
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            switch(event.pos)
            draw(event.pos)
        if event.type == pygame.KEYUP:
            if event.key == 112:
                play = (play+1)%2
            if event.key == 103:
                grid = (grid+1)%2
                if grid == 0:
                    drawgrid(0,0,0)
    
    draw_on_curtain(life1, pygame.time.get_ticks() / 1000.0)    
    pygame.display.flip()
    clock.tick(30)
