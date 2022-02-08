import pygame as pg
from settings import *

class Desktop:
    """ Represents the desktop view """

    def __init__(self, app):
        self.app = app
        self.icons = []
        self.taskbar: TaskBar = None


class TaskBar:
    """ Represents the task bar from which the user can launch programs """

    def __init__(self, app):
        self.app = app
        self.icons = []

class Icon(pg.sprite.Sprite):
    """ Represents a program icon """

    def __init__(self, app, img):
        self.app = app
        self.groups = app.icons
        pg.sprite.Sprite.__init__(self, self.groups)
        self.screen = app.screen
        self.image = img
        self.rect = img.get_rect()
        self.rect.x = 200
        self.rect.y = 300

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def events(self, event):
        now = pg.time.get_ticks()
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True