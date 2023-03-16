# -*- coding: utf-8 -*-

"""
Cannon drawn by me in Inkscape

Background by ramses2099: https://opengameart.org/content/background-2
"""

import pygame as pg
from pylab import *
from pygame.locals import *
from pygame.font import *
import sys
import random
from math import pi, sin, cos, sqrt, atan2


pg.init()


screenWidth = 850
screenHeight = 550


screenSize = (screenWidth, screenHeight)

win = pg.display.set_mode(screenSize)

pg.display.set_caption("Cannonball game")



#RGB
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
RED = (255, 0, 0)
DARKGRAY = (128, 128, 128)
TARGETCOLOR = (255, 50, 50)

# Empty list for backgrounds
bgList = []

# Filling the list with background images, scaled by the screen size
for i in range(1, 4+1):
    bg = pg.image.load(f'Graphics/airadventurelevel{i}.png')
    bgList.append(pg.transform.scale(bg, (screenWidth, screenHeight)))




class Cannonball(object):
    def __init__(self, screenSize, v0=90, angle=45):
        self.screenSize = screenSize
        
        self.r = 7
        self.color = BLACK
        self.k = 0
        
        g = 9.81 #m/s**2
        
        x0 = 0
        y0 = 0
        
        v0 /= 3.6 #convert from km/h to m/s
        
        angle = (angle*pi)/180 #convert from degrees to radians
        v0x = v0*cos(angle)
        v0y = v0*sin(angle)
        
        def x(t):
            return x0 + v0x*t
        
        def y(t):
            return y0 + v0y*t - 0.5*g*t**2
        
        
        self.x_vec = [x0]
        self.y_vec = [y0]    
        
        t = 0
        dt = 0.02 #s

        while y(t) >= 0:
            t += dt
            y_tmp = y(t)
            
            if y(t) < 0.0:
                y_tmp = 0.0
            
            self.x_vec.append(x(t))
            self.y_vec.append(y_tmp)
    
    
    
    def render(self, win):
        pg.draw.circle(win, self.color, self.center, self.r)
    
    
        
    def update(self):
        sf = 10 #scale factor

        self.x = int(self.x_vec[self.k]*sf)
        self.y = int(self.y_vec[self.k]*sf)
        
        N = len(self.x_vec)
        
        if self.k < N-1:
            self.k += 1
            
        self.y = self.screenSize[1]-self.y
        
        self.center = [self.x, self.y]




class Target(object):
    def __init__(self, screenSize):
        self.screenSize = screenSize
        
        self.color = TARGETCOLOR
        
        self.r = 30 - 3*level
        
        if self.r <= 10:
            self.r = 10
        
        self.x = random.randint(self.r + 50, self.screenSize[0]-self.r - 50)
        self.y = random.randint(self.r + 50, self.screenSize[1]-self.r - 50)
        
        #self.x = 450
        #self.y = 350
        
        
    def render(self, win):
        pg.draw.circle(win, self.color, self.center, self.r)


    def update(self):
        self.center = [self.x, self.y]




class Cannon(pg.sprite.Sprite):
    def __init__(self):
        self.cannonImg = pg.image.load('Graphics/cannon.png')
        self.pivot = (0, screenHeight)
        self.angle = 0
        self.aimCannon()


    def aimCannon(self):
        # rotate the cannon image around the pivot
        self.image = pg.transform.rotate(self.cannonImg, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pivot
        
        
    def update(self, mPos):
        # set angle between the cannon and mouse pos
        yDiff = self.rect.centery - mPos[1] 
        xDiff = mPos[0] - self.rect.centerx 
        self.angle = atan2(yDiff, xDiff)*180/pi
        self.aimCannon()
    
    def draw(self, win):
        win.blit(self.image, self.rect)
        



def display_text(message, fontsize):
    font1 = pg.font.SysFont('Verdana', fontsize)
    text = font1.render(message, True, BLACK, WHITE)
    
    textRect = text.get_rect()
    textRect.center = (screenWidth/2, screenHeight/2)
    
    win.blit(text, textRect)
    
    pg.display.update()
    



def paused():
    global ammo
    global hit
    global level
    
    if ammo <= 0 and not hit:
        display_text("Out of ammo!", 100)
        level = 0
        message = "Play again"
    
    elif hit:
        display_text("You hit!", 100)
        message = "Next level"
    
        
    while True:
        w = 120
        h = 60
        
        button(message, (screenWidth/4) - w/2, (screenHeight/4)*3,
               w, h, WHITE, main)
        
        button("Quit", (screenWidth/4)*3 - w/2, (screenHeight/4)*3,
               w, h, WHITE, quitgame)
        
        
        event = pg.event.wait()
        
        if event.type == pg.QUIT:
            quitgame()
        



def button(message, x,y,w,h, color, action=None):
    mousePos = pg.mouse.get_pos()
    click = pg.mouse.get_pressed()
    
    pg.draw.rect(win, color, (x,y,w,h))
    
    if x < mousePos[0] < x+w and y < mousePos[1] < y+h:
        if click[0] == 1 and action != None:
            action()
            
        
    font = pg.font.Font('freesansbold.ttf', 20)
    text = font.render(message, True, BLACK)
    
    textRect = text.get_rect()
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    
    win.blit(text, textRect)
    
    pg.display.update()



def quitgame():
    pg.display.quit()
    pg.quit()
    sys.exit()
    quit()
    


def check_collision(ball, target):
    global hit
    d = sqrt((ball.center[0] - target.center[0])**2 + \
            (ball.center[1] - target.center[1])**2)
        
    rtot = ball.r + target.r
    
    if d <= rtot:
        hit = True
        paused()



def shoot(v0, angle):
    global screenSize
    global balls
    global ammo
    
    if ammo <= 0:
        paused()
    
    if ammo > 0:
        ammo -= 1
        balls.append(Cannonball(screenSize, v0, angle))



clock = pg.time.Clock()
FPS = 60

level = 0

def main():   
    global win
    global screenSize
    global balls
    global ammo
    global level
    global hit
    
    #bg = random.choice(bgList)
    bg = bgList[level//3]
    
    hit = False
    
    level += 1
    
    run = True
    clock.tick(FPS)
    
    target = Target(screenSize)
    cannon = Cannon()
    
    v0 = 100 #km/h
    angle = 45 #degrees
    
    mousePos = (screenWidth/2, screenHeight/2)
    

    #ammo = 5
    ammo = 10 - level
    
    if ammo <= 0:
        ammo = 1
    
    
    balls = []
    
    while run:
        win.blit(bg, (0,0))
        

        
        for e in pg.event.get():
            if e.type == pg.MOUSEMOTION:
                mousePos = pg.mouse.get_pos()
                
            if e.type == pg.KEYDOWN:
                """
                if e.key == pg.K_w:
                    angle += 5
                if e.key == pg.K_s:
                    angle -= 5
                """
                if e.key == pg.K_d:
                    v0 += 10
                if e.key == pg.K_a:
                    v0 -= 10
                if e.key == pg.K_SPACE:
                    shoot(v0, angle)
            
            

            if e.type == pg.MOUSEBUTTONDOWN:
                if pg.mouse.get_pressed()[0]:
                    shoot(v0, angle)
                if e.button == 4:
                    v0 += 10
                elif e.button == 5:
                    v0 -= 10
            
            if v0 > 150:
                v0 = 150
                
            if v0 < 50:
                v0 = 50
            
            
            if e.type == pg.QUIT:
                quitgame()
        
        
             
        
        cannon.update(mousePos)
        
        angle = cannon.angle
        
        
        font1 = pg.font.SysFont('Verdana', 25)
        font2 = pg.font.SysFont('Verdana', 40)
        
        angleTextImg = font1.render(f" Angle: {angle:.0f}° ", True, BLACK, WHITE)
        v0TextImg = font1.render(f" Initial velocity: {v0} km/h ", True, BLACK, WHITE)
        ammoTextImg = font1.render(f" Ammo left: {ammo} ", True, BLACK, WHITE)
        levelTextImg = font2.render(f" Level: {level:2d} ", True, BLACK, WHITE)
        
        win.blit(angleTextImg, (0,0))
        win.blit(v0TextImg, (0,angleTextImg.get_height()))
        win.blit(ammoTextImg, (0, angleTextImg.get_height() + v0TextImg.get_height()))
        
        
        target.update()
        target.render(win)
        
        for ball in balls:
            ball.update()
            ball.render(win)
            check_collision(ball, target)
            
        cannon.draw(win)
        
        win.blit(levelTextImg, (screenWidth-levelTextImg.get_width(),0))
        
        
        #pg.display.flip()
        pg.display.update()
        
        


#Run the game
main()


quitgame()
