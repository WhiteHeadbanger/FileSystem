import pygame as pg

class Terminal:

    def __init__(self, game) -> None:
        self.image = pg.Surface((500, 400))
        self.game = game
        self.rect = self.image.get_rect()
        self.image.fill((0, 0, 0))
        
        self.make()

    def make(self):
        self.output()
        self.input()

    def output(self):
        pg.draw.rect(self.image, color = (50, 50, 50), rect=(20, 20, 400, 350))
    
    def input(self):
        pg.draw.rect(self.image, color = (50, 50, 50), rect=(20, 390, 400, 350))

    def draw(self):
        self.game.screen.blit(self.image, self.rect)
