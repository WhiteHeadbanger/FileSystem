import json
import sys
from typing import Optional, Dict
from .computer import Computer

class FileSystem:

    def __init__(self, name: str, parent: Optional["Directory"], owner: int, group_owner: int):
        self.name: str = name
        self.parent = parent
        self.owner = owner
        self.group_owner = group_owner
        self.permissions: Dict[str, str] = {}
        self.size: int
        self.path: str

    def is_dir(self):
        return type(self) == Directory

    def is_file(self):
        return type(self) == File

class Directory(FileSystem):

    def __init__(self, name, parent, owner, group_owner):
        super().__init__(name, parent, owner, group_owner)
        self.files = {}
        self.size = None

    def add_file(self, file):
        if file.name not in self.files.keys():
            self.files[file.name] = file


class File(FileSystem):

    def __init__(self, name: str, content: str, parent: Optional["Directory"], owner: int, group_owner: int):
        super().__init__(name, parent, owner, group_owner)
        self.content = content
        self.size = sys.getsizeof(self.name + self.content)

class StdFS:

    def __init__(self, computer: Computer):
        self.computer = computer
        self.root = Directory("/", None, 0, 0)

        self.initialize()

    def initialize(self):
        root_directories = ["bin", "home", "lib", "root", "usr"]
        for dir in root_directories:
            directory = Directory(dir, self.root, 0, 0)
            self.root.add_file(directory)

