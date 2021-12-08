import pygame as pg

import json
import os, sys

from gui import Terminal

class Game:

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((900, 900))
        self.clock = pg.time.Clock()

    def load_data(self):
        pass

    def new_game(self):
        self.load_gui()

    def run(self):
        self.running = True
        while self.running:
            self.dt = self.clock.tick(60)
            self.draw()
            self.events()
    
    def quit(self):
        pg.quit()
        sys.exit()
        
    def load_gui(self):
        self.terminalGui = Terminal(self)

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.terminalGui.draw()
        pg.display.flip()

    def events(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.quit()

if __name__ == '__main__':
    g = Game()
    g.new_game()
    while True:
        g.run()