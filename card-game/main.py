import pygame as pg
import random
import numpy as np
from settings import *
from sprites import *


# Game class
class Game:
    def __init__(self):
        pg.init()

        self.screen = pg.display.set_mode(SIZE)

        pg.display.set_caption("Card Game")

        self.clock = pg.time.Clock()

        self.running = True

    def new(self):
        self.hand = []
        self.deck = []
        self.discard = []
        self.active_card = None

        self.hand.append(Card())

        self.run()

    def run(self):
        # Game loop
        self.playing = True

        while self.playing:
            self.clock.tick(FPS)
            self.active_card = None
            self.events()
            self.update()
            self.draw()


    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False

                self.running = False
                
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for num, card in enumerate(self.hand):
                        if pg.Rect.collidepoint(card.rect, event.pos):
                            self.active_card = num
                            print(self.active_card)
                            
            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    self.active_card = None
                
            if event.type == pg.MOUSEMOTION:
                if self.active_card != None:
                    print("Move")
                    self.hand[self.active_card].rect.move_ip(event.rel)
                    print(self.hand[self.active_card].rect)
                

    def update(self):
        pass

    def draw(self):
        self.screen.fill(GREY)

        for num, card in enumerate(self.hand):
            self.screen.blit(card.image, (card.rect.x, card.rect.y))
            pg.draw.rect(card.image, BLACK, [0, 0, CARD_WIDTH, CARD_HEIGHT], 2)

        pg.display.flip()



game_object = Game()

while game_object.running:
    game_object.new()


pg.quit()
