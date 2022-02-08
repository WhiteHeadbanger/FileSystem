import pygame as pg
from window import StdWindow, Terminal
from desktop import Icon
from typing import List
import sys
from os import path

class OS:

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((1920, 1080))
        self.screen_rect = self.screen.get_rect()
        pg.display.set_caption("Virtual File System")
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)

        self.open_windows = []
        self.wallpaper = None
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')

        self.terminal_icon = pg.image.load(path.join(img_folder, 'terminal.png')).convert_alpha()
        self.folder_icon = pg.image.load(path.join(img_folder, 'folder.png')).convert_alpha()

    def new(self):
        """ Initialize variables and do initial setup """

        self.icons = pg.sprite.Group()
        self.font = pg.font.SysFont("Arial", 15)
        #self.terminal_window = Terminal(self, 400, 400, "Terminal Test")
        self.terminal_icon = Icon(self, self.terminal_icon)

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
        for window in self.open_windows:
            window.draw()
        self.terminal_icon.draw()
        pg.display.flip()

    def events(self):
        execute_terminal = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            
            for window in self.open_windows:
                window.events(event)
                
            execute_terminal = self.terminal_icon.events(event)
        
        if execute_terminal:
            self.open_windows.append(Terminal(self, 200, 200, "Terminal"))

if __name__ == '__main__':
    root = OS()
    root.new()
    while True:
        root.run()


