import pygame as pg
import random
import numpy as np
from settings import *
from cards import *


class Bottom:
    def __init__(self):
        self.image = pg.Surface((TABLE_WIDTH, TABLE_HEIGHT))
        self.image.fill(TABLE_COLOR)
        
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = HEIGHT - TABLE_HEIGHT
        
    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))
    
    def checkCollision(self, obj):
        self.update()
        return pg.Rect.colliderect(self.rect, obj.rect)


screen = pg.display.set_mode(SIZE)
pg.display.set_caption(TITLE)
clock = pg.time.Clock()


hand = []
deck = []
discard = []

bottom = Bottom()

for i in range(5):
    hand.append(Card(180*(i+1), HEIGHT - CARD_HEIGHT//2))

active_card = None
run = True

while run:
    clock.tick(FPS)
    
    for event in pg.event.get():
        for num, card in enumerate(hand):
            if card.rect.collidepoint(pg.mouse.get_pos()):
                hover_card = True
            
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                for num, card in enumerate(hand):
                    if pg.Rect.collidepoint(card.rect, event.pos):
                        active_card = num
                        pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
                        
        if event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    #print(hand[active_card].rect)
                    active_card = None
                    pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
        
        if event.type == pg.MOUSEMOTION:
            if active_card != None:
                hand[active_card].rect.move_ip(event.rel)
    
        if event.type == pg.QUIT:
            run = False
  
    
    screen.fill(GRAY80)
    
    bottom.draw()

    for num, card in enumerate(hand):
        card.draw(screen)

    pg.display.flip()


pg.quit()
