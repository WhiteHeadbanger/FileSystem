import pygame as pg
from settings import *
from random import randint
from typing import Optional

class Desktop:
    """ Represents the desktop view """

    def __init__(self, app):
        self.app = app
        self.icons = []
        self.taskbar: TaskBar = None


class TaskBar:
    """ Represents the task bar from which the user can launch programs """

    def __init__(self, app, x, y):
        self.app = app
        self.screen = app.screen
        self.taskbar = pg.rect.Rect(x, y, SCREEN_WIDTH, TASKBAR_HEIGHT)
        self.color = (143, 53, 155)
        self.icons: Icon = []

    def add_icon(self, icon):
        icon.thumbnail_rect.x += 96 * len(self.icons)
        self.icons.append(icon)

    def draw(self):
        pg.draw.rect(self.screen, self.color, self.taskbar)
        if self.icons:
            self.draw_icons()

    def draw_icons(self):
        for icon in self.icons:
            self.screen.blit(icon.thumbnail, icon.thumbnail_rect)

class Icon(pg.sprite.Sprite):
    """ Represents a program icon on the desktop """

    def __init__(self, app, x, y, img = None, thumbnail = None):
        self.id = randint(0, 100)
        self.app = app
        self.thumbnail = thumbnail
        self.groups = app.icons
        pg.sprite.Sprite.__init__(self, self.groups)
        self.screen = app.screen
        self.image = img 
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.thumbnail_rect = self.thumbnail.get_rect()
        self.thumbnail_rect.x = x
        self.thumbnail_rect.y = y
        self.last_click = 1000
        # In taskbar
        self.pinned: bool = False

        self.offsetX = 0
        self.offsetY = 0
        self.drag = False
        # The ghost is a ghost copy (a copy with transparency) that is created whem the icon is dragged. When the drag finishes, it is erased from view.
        self.ghost: Icon = None
        


    def draw(self):
        if self.ghost:
            self.ghost.screen.blit(self.ghost.image, self.ghost.rect)
        self.screen.blit(self.image, self.rect)

    def events(self, event):
        now = pg.time.get_ticks()
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.drag = True
                if now - self.last_click <= DOUBLE_CLICK_TIMER:
                    return True
                self.last_click = now

        elif event.type == pg.MOUSEMOTION:
            if self.drag:
                mouseX, mouseY = event.pos
                if self.ghost and self.ghost.drag:
                    self.ghost_drag(mouseX, mouseY)
                    return
                
                self.ghost = Icon(self.app, x=self.rect.x, y=self.rect.y, img=self.image.copy(), thumbnail=self.thumbnail.copy())
                self.ghost.image.set_alpha(175)
                self.ghost.drag = True
                self.ghost_drag(mouseX, mouseY)

        elif event.type == pg.MOUSEBUTTONUP:
            self.drag = False
            if self.ghost:
                self.icon_drop(event)
                self.ghost = None

    def ghost_drag(self, mouseX, mouseY):
        self.ghost.rect.x, self.ghost.rect.y = mouseX + self.ghost.offsetX, mouseY + self.ghost.offsetY
        self.ghost.offsetX, self.ghost.offsetY = self.ghost.rect.x - mouseX, self.ghost.rect.y - mouseY
        self.ghost.draw()

    def icon_drop(self, event):
        if self.ghost.rect.collidepoint(event.pos) and self.app.taskbar.taskbar.collidepoint(event.pos):
            self.app.taskbar.add_icon(Icon(self.app, x = 100, y = SCREEN_HEIGHT - 50, img = self.image.copy(), thumbnail = self.thumbnail.copy()))
            self.pinned = True
            return
        self.rect.x, self.rect.y = self.ghost.rect.x, self.ghost.rect.y