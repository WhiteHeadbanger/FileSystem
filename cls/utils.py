from enum import Enum
from abc import ABC, abstractmethod

class ParserBase(ABC):

    @abstractmethod
    def __init__(self, path):
        raise NotImplementedError

    @abstractmethod
    def parse(self, args):
        raise NotImplementedError

class Parser(ParserBase):

    def __init__(self, path):
        self.path = path

    def parse(self, args):
        params = [arg for arg in args.split().split('/')]
        if params[0] in self.path:
            pass

