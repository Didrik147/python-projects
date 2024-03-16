import pygame as pg
from settings import *

pg.init()
font = pg.font.SysFont("Tahoma", 20)

class Card:
    def __init__(self, x, y):
        self.image = pg.Surface((CARD_WIDTH, CARD_HEIGHT))
        self.image.fill(WHITE)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.text = "Card name"
        
        
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        pg.draw.rect(self.image, BLACK, [0, 0, CARD_WIDTH, CARD_HEIGHT], 2)
        
        textImg = font.render(self.text, True, BLACK)
        textRect = textImg.get_rect()
        screen.blit(textImg, 
                    (self.rect.x + CARD_WIDTH//2 - textRect.width//2, self.rect.y + 10)
        )
