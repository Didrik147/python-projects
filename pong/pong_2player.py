# Importing libraries
import pygame as pg
import random

# Constants
WIDTH = 700  # width of window
HEIGHT = 500 # height of window
SIZE = (WIDTH, HEIGHT) # window size

FPS = 60 # frames per second

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MYCOLOR = (100, 200, 50)

# Initialize pygame
pg.init()

# Creates a surface we can draw on
surface = pg.display.set_mode(SIZE)

pg.display.set_caption('Pong')

# Creates a clock
clock = pg.time.Clock()

# Sound
pg.mixer.init()

# Collision sound
pong_sound = pg.mixer.Sound('./snd/pong.ogg')
pong_sound.set_volume(0.5)
ping_sound = pg.mixer.Sound('./snd/ping.ogg')
ping_sound.set_volume(0.5)

collision_sounds = [pong_sound, ping_sound]


class Ball:
    def __init__(self, x=WIDTH//2, y=HEIGHT//2, r=15, color=WHITE):
        self.x = x
        self.y = y
        self.r = r
        #self.color = color
        self.color = YELLOW
        
        # Velocity
        #self.vx = random.choice([-1,1])*5
        self.vx = 0
        self.vy = random.choice([-1,1])*4
 
        
    # Method for drawing figure
    def draw(self):
        center = (self.x, self.y)
        pg.draw.circle(surface, self.color, center, self.r)
        
        
    # Method for drawing figure
    def update(self):
        # Change position based on velocity
        self.x += self.vx
        self.y += self.vy
        
            
        # Check collision with top
        if self.y - self.r <= 0:
            self.vy *= -1
            self.y = self.r
        
        # Check collision with bottom
        if self.y + self.r >= HEIGHT:
            self.vy *= -1
            self.y = HEIGHT - self.r



class Paddle:
    def __init__(self, x, y, w, h, color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        
        self.vx = 0
        self.vy = 0
        
        self.speed = 7
        
    def draw(self):
        rect = pg.Rect(self.x, self.y, self.w, self.h)
        pg.draw.rect(surface, self.color, rect)
        
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
            
        if self.y <= 0:
            self.vy *= -1
            self.y = 0

        if self.y + self.h >= HEIGHT:
            self.vy *= -1
            self.y = HEIGHT - self.h



w = 20
h = 120


class LeftPlayer(Paddle):
    def __init__(self):
        super().__init__(0, HEIGHT//2, w, h, WHITE)
        self.name = "WASD"
        
    def move(self):
        self.vy = 0
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.vy = -self.speed
        
        if keys[pg.K_s]:
            self.vy = self.speed
    

class RightPlayer(Paddle):
    def __init__(self):
        super().__init__(WIDTH-w, HEIGHT//2, w, h, WHITE)
        self.name = "Arrow keys"
        
    def move(self):
        self.vy = 0
        keys = pg.key.get_pressed()
        if keys[pg.K_UP]:
            self.vy = -self.speed
        
        if keys[pg.K_DOWN]:
            self.vy = self.speed


# Choosing font and fontsize
font = pg.font.SysFont("Arial", 30)

score1 = 0 # left player score
score2 = 0 # right player score

def drawScore():
    textLeft = font.render(f'Score: {score1}', True, WHITE)
    textRight = font.render(f'Score: {score2}', True, WHITE)
    
    rectLeft = textLeft.get_rect()
    rectRight = textRight.get_rect()
    
    surface.blit(textLeft, (WIDTH//4 - rectLeft.width//2, 0))
    surface.blit(textRight, (WIDTH*3//4 - rectRight.width//2, 0))
    
    
    
def drawText(text, x, y, fontSize):
    font = pg.font.SysFont("Arial", fontSize)
    textImg = font.render(text, True, WHITE)
    
    rect = textImg.get_rect()
    
    surface.blit(textImg, (x - rect.width//2, y - rect.height//2))



def drawNet():
    pg.draw.line(surface, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT), width=10)
    
    for i in range(0, HEIGHT, 40):
        start_pos = (WIDTH//2, i+20)
        end_pos = (WIDTH//2, i+30)
        pg.draw.line(surface, BLACK, start_pos, end_pos, width=10)




ball = Ball()

paddle1 = LeftPlayer()
paddle2 = RightPlayer()

paddle1.color = (255,50,50)
paddle2.color = GREEN


def collision(ball, paddle1, paddle2):
    # Left
    if ball.vx < 0:
        if ball.x - ball.r <= paddle1.x + paddle1.w:
            if ball.y + ball.r >= paddle1.y and ball.y - ball.r <= paddle1.y + paddle1.h:
                #ball.vx *= -1
                ball.vx *= -1.05
                
                middle_y = paddle1.y + paddle1.h//2
                dy = middle_y - ball.y
                
                ball.vy = -1*dy//10
                
                random.choice(collision_sounds).play()
        
    # Right
    if ball.vx > 0:
        if ball.x + ball.r >= paddle2.x:
            if ball.y + ball.r >= paddle2.y and ball.y - ball.r <= paddle2.y + paddle2.h:
                #ball.vx *= -1
                ball.vx *= -1.05
                
                middle_y = paddle2.y + paddle2.h//2
                dy = middle_y - ball.y
                
                ball.vy = -1*dy//10
                
                random.choice(collision_sounds).play()
        



def tilfeldigFarge():
    R = random.randint(0, 255)
    G = random.randint(0, 255)
    B = random.randint(0, 255)
    
    return (R, G, B)    



run = True

gameOver = False


# Game loop
while run:
    clock.tick(FPS)
    
    for event in pg.event.get():
        # Checking if we want to close the window
        if event.type == pg.QUIT:
            run = False
            
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE and ball.vx == 0:
                ball.vx = random.choice([-1,1])*5
                
        
    surface.fill(BLACK)
    
    collision(ball, paddle1, paddle2)
    
    if ball.x + ball.r < 0:
        score2 += 1
        drawText(f'"{paddle2.name}" gained a point!', WIDTH//2, HEIGHT//2, 60)
        paddle1.draw()
        paddle2.draw()
        drawScore()
        pg.display.flip()
        
        pg.time.wait(1500)
        
        ball = Ball()
        
    if ball.x - ball.r > WIDTH:
        score1 += 1
        drawText(f'"{paddle1.name}" gained a point!', WIDTH//2, HEIGHT//2, 60)
        paddle1.draw()
        paddle2.draw()
        drawScore()
        pg.display.flip()
        
        pg.time.wait(1500)
        
        ball = Ball()
        
    if not gameOver:
        drawNet()
        
        ball.update()
        ball.draw()
        
        paddle1.move()
        paddle1.update()
        paddle1.draw()
        
        paddle2.move()
        paddle2.update()
        paddle2.draw()
        
        
        drawScore()
        
    
    if score1 >= 3:
        drawText(f'"{paddle1.name}" won!', WIDTH//2, HEIGHT//2, 60)
        gameOver = True
    elif score2 >= 3:
        drawText(f'"{paddle2.name}" won!', WIDTH//2, HEIGHT//2, 60)
        gameOver = True
    
    # After drawing everything, we flip the display
    pg.display.flip()


# Closing pygame
pg.quit()






