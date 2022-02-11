import pygame as pg
from window import StdWindow, Terminal, ContextMenu, Folder
from desktop import Icon, TaskBar
from typing import List
import sys
from os import path
from random import randint
from settings import *

class OS:

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen_rect = self.screen.get_rect()
        pg.display.set_caption("Virtual File System")
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)

        self.open_windows: List[StdWindow] = []
        self.focused_window: StdWindow = None
        self.context_menu: ContextMenu = None
        self.wallpaper = None
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        self.img_folder = path.join(game_folder, 'img')

        # DESKTOP IMAGE
        self.terminal_desktop_image = pg.image.load(path.join(self.img_folder, 'terminal.png')).convert_alpha()
        self.folder_desktop_image = pg.image.load(path.join(self.img_folder, 'folder.png')).convert_alpha()

        #THUMBNAILS
        self.terminal_thumbnail_image = pg.image.load(path.join(self.img_folder, 'terminal_thumbnail.png')).convert_alpha()
        self.folder_thumbnail_image = pg.image.load(path.join(self.img_folder, 'folder_thumbnail.png')).convert_alpha()

    def new(self):
        """ Initialize variables """

        self.icons = pg.sprite.Group()
        self.font = pg.font.SysFont("Arial", 15)
        self.terminal_icon = Icon(self, x = 100, y = 100, program_associated = "Terminal", img = self.terminal_desktop_image, thumbnail=self.terminal_thumbnail_image)
        self.folder_icon = Icon(self, x = 100, y = 250, program_associated = "Folder", img = self.folder_desktop_image, thumbnail=self.folder_thumbnail_image)
        self.taskbar = TaskBar(self, x=0, y=SCREEN_HEIGHT - TASKBAR_HEIGHT)

    def run(self):
        
        self.running = True
        while self.running:
            self.dt = self.clock.tick(FPS)
            self.draw()
            self.events()

    def quit(self):
        pg.quit()
        sys.exit()

    def draw(self):
        self.screen.fill(SCREEN_WALLPAPER)
        self.taskbar.draw()
        self.terminal_icon.draw()
        self.folder_icon.draw()
        for window in self.open_windows[::-1]:
            window.draw()
        if self.context_menu:
            self.context_menu.draw()
        pg.display.flip()

    def events(self):
        execute_terminal = False
        execute_folder = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
                mouseX, mouseY = event.pos
                self.context_menu = ContextMenu(self, mouseX, mouseY, ["Opt1", "Opt2", "Opt3"])

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                self.context_menu = None

            for window in self.open_windows:
                if event.type == pg.MOUSEBUTTONDOWN and window.window.collidepoint(event.pos) and event.button == 1:
                    window.focused = True
                    self.focused_window = window
                    self.open_windows.insert(0, self.open_windows.pop(self.open_windows.index(window)))
                    break

            for window in self.open_windows:
                if self.focused_window != window:
                    window.focused = False
                window.events(event)
                    
            execute_terminal = self.terminal_icon.events(event)
            execute_folder = self.folder_icon.events(event)

        if execute_terminal:
            self.open_windows.append(Terminal(self, 200, 200, f"Terminal - {randint(0, 100)}"))
        elif execute_folder:
            self.open_windows.append(Folder(self, 200, 200, f"Folder - {randint(0, 100)}", self.folder_desktop_image))



if __name__ == '__main__':
    root = OS()
    root.new()
    while True:
        root.run()


