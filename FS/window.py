import pygame as pg
from typing import Any, Union, Optional

class StdWindow(pg.sprite.Sprite):

    def __init__(self, app, x, y, title):
        self.app = app
        self.screen = app.screen
        self.title = title
        self.window = pg.rect.Rect(x, y, 600, 400)
        self.color = (0, 0, 0)
        self.title_bar = pg.rect.Rect(x, y, 600, 25)
        self.title_bar_color = (77, 77, 77)
        self.title_text = app.font.render(title, True, (255, 255, 255)) 
        self.focused = False
        self.parent = None
        self.minimized = False
        self.drag = False
        self.offsetX = 0
        self.offsetY = 0

    def draw(self):
        pg.draw.rect(self.screen, self.color, self.window)
        pg.draw.rect(self.screen, self.title_bar_color, self.title_bar)
        # Calculate the position of the title text
        text_rect = self.title_text.get_rect(center=self.title_bar.center)
        self.screen.blit(self.title_text, text_rect)

    def events(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.title_bar.collidepoint(event.pos):
                self.drag = True
                mouseX, mouseY = event.pos
                self.offsetX = self.window.x - mouseX
                self.offsetY = self.window.y - mouseY
                

        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.drag = False

        elif event.type == pg.MOUSEMOTION:
            if self.drag and self.focused:
                mouseX, mouseY = event.pos
                self.drag_window(mouseX + self.offsetX, mouseY + self.offsetY)

    def drag_window(self, x, y):
        self.window.x, self.window.y = x, y
        self.title_bar.x, self.title_bar.y = x, y

    def update(self):
        pass


class Terminal(StdWindow):

    def __init__(self, app, x, y, title):
        super().__init__(app, x, y, title)
        self.text = ""
        self.history = []

    def events(self, event):
        super().events(event)
        if event.type == pg.KEYDOWN:
            if self.focused:
                if event.key == pg.K_RETURN:
                    self.history.append(self.text)
                    self.text = ""
                else:
                    self.text += event.unicode

    def draw(self):
        super().draw()

    def update(self):
        pass



        
