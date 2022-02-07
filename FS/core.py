import pygame as pg
from window import StdWindow, Terminal
from typing import List
import sys

class OS:

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((1920, 1080))
        self.screen_rect = self.screen.get_rect()
        pg.display.set_caption("Virtual File System")
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)

        self.open_windows = List[StdWindow]
        self.wallpaper = None

    def new(self):
        """ Initialize variables and do initial setup """

        self.font = pg.font.SysFont("Arial", 15)
        self.terminal_window = Terminal(self, 400, 400, "Terminal Test")

    def run(self):
        
        self.running = True
        while self.running:
            self.dt = self.clock.tick(60)
            self.draw()
            self.events()

    def quit(self):
        pg.quit()
        sys.exit()

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.terminal_window.draw()
        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            self.terminal_window.events(event)

if __name__ == '__main__':
    root = OS()
    root.new()
    while True:
        root.run()


