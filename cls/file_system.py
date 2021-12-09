import json
import sys, os
from typing import Optional, Dict
from os import path
from .computer import Computer
from .user import User

__THIS_FOLDER__ = path.dirname(__file__)
__BIN__ = path.join(__THIS_FOLDER__, 'bin')
__HOME__ = path.join(__THIS_FOLDER__, 'home')
__LIB__ = path.join(__THIS_FOLDER__, 'lib')
__ROOT__ = path.join(__THIS_FOLDER__, 'root')
__USR__ = path.join(__THIS_FOLDER__, 'usr')

class FileSystem:

    def __init__(self, name: str, parent: Optional["Directory"], owner: int, group_owner: int):
        self.name: str = name
        self.parent = parent
        self.owner = owner
        self.group_owner = group_owner
        self.permissions: Dict[str, str] = {}
        self.size: int

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

    def find(self, file):
        return self.files.get(file, None)

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
        root_directories = ['bin', 'etc', 'home', 'lib', 'root', 'usr']
        for dir in root_directories:
            directory = Directory(dir, self.root, 0, 0)
            self.root.add_file(directory)

        self.init_bin()
        self.init_etc()
        #self.init_home()
        #self.init_lib()
        #self.init_root()
        #self.init_usr()

    def init_bin(self):
        bin_dir = self.root.find('bin')
        files = os.listdir(__BIN__)
        for file in files:
            path = __BIN__ + f'/{file}'
            with open(path, 'r') as f:
                if file not in ['__init__.py']:
                    bin_file = File(file, f.read(), self.root.files['bin'], 0, 0)
                    bin_dir.add_file(bin_file)
    
    def init_etc(self):
        etc_dir = self.root.find('etc')
        skeleton: Directory = Directory('skeleton', etc_dir, 0, 0)

        etc_dir.add_file(skeleton)

        folders = ['Desktop', 'Downloads', 'Pictures', 'Music']
        for folder in folders:
            d: Directory = Directory(folder, skeleton, 0, 0)
            skeleton.add_file(d)

    """ def init_lib(self):
        home_dir = self.root.find("home")

        user: User = self.computer.get_session()
        user = user.username
        user_dir = Directory(user, home_dir, 0, 0)
        
        self.home_dir.add_file(user_dir)

    def init_root(self):
        home_dir = self.root.find("home")

        user: User = self.computer.get_session()
        user = user.username
        user_dir = Directory(user, home_dir, 0, 0)
        
        self.home_dir.add_file(user_dir)

    def init_usr(self):
        home_dir = self.root.find("home")

        user: User = self.computer.get_session()
        user = user.username
        user_dir = Directory(user, home_dir, 0, 0)
        
        self.home_dir.add_file(user_dir) """

