import pygame as pg
from settings import *


class Card:
    def __init__(self):
        self.image = pg.Surface((CARD_WIDTH, CARD_HEIGHT))
        self.image.fill(WHITE)
        
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = HEIGHT - CARD_HEIGHT - 20

    def update(self):
        pass
