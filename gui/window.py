import pygame as pg
from typing import Any, Union, Optional, List
from os import path

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
        self.scroll = False
        self.resizable = True


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
                

        elif event.type == pg.MOUSEBUTTONUP:
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

class Folder(StdWindow):

    def __init__(self, app, x, y, title):
        super().__init__(app, x, y, title)
        self.x = x
        self.y = y
        self.files = []
        self.parent: Optional[Folder] = None
        self.color = (255, 255, 255)

    def add_file(self, file):
        self.files.append(file)

    def del_file(self, file):
        self.files.pop(self.files.index(file))

    def draw(self):
        super().draw()
        for file in self.files:
            self.screen.blit(file.image, file.rect)

    def events(self, event):
        super().events(event)
        if event.type == pg.MOUSEMOTION:
            if self.drag and self.focused:
                for file in self.files:
                    file.rect.x, file.rect.y = self.window.x + 50, self.window.y + 50
        

class ContextMenu:
    """ Represents the context menu that appears when the user right clicks on files, folders, the desktop or application. """

    def __init__(self, app, x, y, options):
        self.app = app
        self.screen = app.screen
        # TODO options SHOULD be a list of classes 'MenuOption'. Maybe ContextMenu AND MenuOption should be a subclass for a Menu class.
        self.options = options
        self.background_color = (190, 190, 190)
        self.text_color = (0, 0, 0)
        self.menu = pg.rect.Rect(x, y, 250, len(options) * 100)
        self.highlight_color = (150, 150, 150)
        """ self.title_text = app.font.render(title, True, (255, 255, 255)) """ 
        self.parent = None
        # Storing the last Y position to draw the options. Starts at 5.
        self.last_y_position = 10

    def draw(self):
        pg.draw.rect(self.screen, self.background_color, self.menu)
        for opt in self.options:
            text = self.app.font.render(opt, True, self.text_color) 
            text_rect = text.get_rect(x = self.menu.x + 10, y = self.menu.y + self.last_y_position)
            self.last_y_position += 50
            self.screen.blit(text, text_rect)

        self.last_y_position = 10

    def events(self):
        pass


class MessageBox(StdWindow):
    """ Represents a box type window that displays a message. It can have one or more buttons. """

    def __init__(self, app, x, y, title):
        super().__init__(app, x, y, title)
        self.scroll = False
        self.resizable = False
        self.window = pg.rect.Rect(x, y, 200, 125)
        self.title_bar = pg.rect.Rect(x, y, 200, 25)
        self.buttons = []

    def add_button(self, label, absolute_position = None):
        if absolute_position:
            x, y = absolute_position

        self.buttons.append(Button(self.app, x, y, label, None))

    def draw(self):
        super().draw()
        for btn in self.buttons:
            btn.draw()

class Button:
    """ Represents a button """

    def __init__(self, app, x, y, label, action):
        self.screen = app.screen
        self.x = x
        self.y = y
        self.label = label
        self.action = action
        self.color = (120, 120, 120)
        self.rect = pg.rect.Rect(x, y, 90, 20)
        self.parent = None
        self.clicked = False

    def draw(self):
        pg.draw.rect(self.screen, self.color, self.rect)

    def events(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.clicked = True
                
        elif event.type == pg.MOUSEBUTTONUP:
            if self.clicked:
                print(self.action)
            self.clicked = False


        


        
