import pygame as pg

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