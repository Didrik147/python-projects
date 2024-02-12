import pygame as pg
import random
import numpy as np

WIDTH = 1280
HEIGHT = 720

SIZE = (WIDTH, HEIGHT)

FPS = 60

# Colors (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LIGHTBLUE = (100, 100, 255)
GREY = (142, 142, 142)
LIGHTRED = (255, 100, 100)


# Card settings
CARD_WIDTH = 140
CARD_HEIGHT = CARD_WIDTH*1.4

screen = pg.display.set_mode(SIZE)
pg.display.set_caption("Card Game")
clock = pg.time.Clock()


class Card:
    def __init__(self, x, y):
        self.image = pg.Surface((CARD_WIDTH, CARD_HEIGHT))
        self.image.fill(WHITE)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


hand = []
deck = []
discard = []

hand.append(Card(100, HEIGHT - CARD_HEIGHT//2))

active_card = None
run = True

while run:
    clock.tick(FPS)
    
    for event in pg.event.get():
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                for num, card in enumerate(hand):
                    if pg.Rect.collidepoint(card.rect, event.pos):
                        active_card = num
                        
        if event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    print(hand[active_card].rect)
                    active_card = None
        
        if event.type == pg.MOUSEMOTION:
            if active_card != None:
                hand[active_card].rect.move_ip(event.rel)
    
        if event.type == pg.QUIT:
            run = False
            
    
    screen.fill(GREY)

    for num, card in enumerate(hand):
        screen.blit(card.image, (card.rect.x, card.rect.y))
        pg.draw.rect(card.image, BLACK, [0, 0, CARD_WIDTH, CARD_HEIGHT], 2)

    pg.display.flip()


pg.quit()
