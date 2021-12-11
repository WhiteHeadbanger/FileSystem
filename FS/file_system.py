import json
import sys, os
from typing import Optional, Dict, List, Union
from os import path
from user import User
from utils import response

__THIS_FOLDER__ = path.dirname(__file__)
__BIN__ = path.join(__THIS_FOLDER__, 'bin')
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
        if file.startswith('/'):
            file = file.split('/')
            del file[0]
            return self.files.get(file[0], None)
        
        return self.files.get(file, None)

    def get_parent(self):
        return self.parent if self.name != '/' else None 

class File(FileSystem):

    def __init__(self, name: str, content: str, parent: Optional[Directory], owner: int, group_owner: int):
        super().__init__(name, parent, owner, group_owner)
        self.content = content
        self.size = sys.getsizeof(self.name + self.content)

    def read(self):
        return self.content

class StdFS:

    def __init__(self, computer: object):
        self.computer = computer
        self.root = Directory("/", None, 0, 0)

        self.initialize()

    def initialize(self):
        root_directories = ['bin', 'etc', 'home', 'lib', 'root', 'usr']
        for dir in root_directories:
            directory = Directory(dir, self.root, 0, 0)
            self.root.add_file(directory)

        self.init_bin()
        #self.init_etc()
        self.init_home()
        #self.init_lib()
        #self.init_root()
        #self.init_usr()

    def get_root(self):
        return self.root

    def make_dir(self, name: str):
        """ Creates a directory in the local path """
        #TODO make absolute path too.

        curr_dir = self.computer.terminal.get_curr_dir()

        _dir = Directory(name, curr_dir, 0, 0)
        curr_dir.add_file(_dir)

    def make_file(self, name: str, content: str):
        """ Creates a file in the local path """
        #TODO make absolute path too.

        curr_dir = self.computer.terminal.get_curr_dir()

        file = File(name, content, curr_dir, 0, 0)
        curr_dir.add_file(file)

    def delete(self, name: str, curr_dir = None):
        if curr_dir is None:
            curr_dir = self.computer.terminal.get_curr_dir()

        file = curr_dir.find(name)
        if file is not None:
            if file.is_file():
                del curr_dir.files[name]
            elif file.files:
                try:
                    for f, v in file.files.items():
                        if v.is_file():
                            del file.files[v.name]
                            continue
                        # If v is not a file
                        curr_dir = v
                        return self.delete(f, curr_dir)
                except RuntimeError:
                    pass
            #del curr_dir.files[name]

    def init_bin(self):
        bin_dir = self.root.find('bin')
        files = os.listdir(__BIN__)
        for file in files:
            if file not in ['__init__.py', '__pycache__', '.vscode']:
                bin_file = File(file.replace(".py", ""), "Cannot read binary data.", bin_dir, 0, 0)
                bin_dir.add_file(bin_file)
    
    def init_home(self):
        home_dir = self.root.find('home')
        user: Directory = Directory(self.computer.session.username, home_dir, 0, 0)

        home_dir.add_file(user)

        def init_user():
            folders = ['Desktop', 'Downloads', 'Pictures', 'Music']
            for folder in folders:
                d: Directory = Directory(folder, user, 0, 0)
                user.add_file(d)  

        return init_user()

    def find_dir(self, path: Union[str, List[str]]) -> Directory:
        """ 
        Finds a specific directory
        returns: Directory 
        """

        # Current directory
        curr_dir = self.computer.terminal.get_curr_dir()

        # If path is referencing /, return root directory (not '/root')
        if path == '/':
            return self.root

        # If path is '..', return parent directory if not root, else return nothing (TODO: standarize response messages)
        if path == '..':
            parent_dir = curr_dir.get_parent()
            if parent_dir is None:
                print("Directory not found.")
                return
            return parent_dir

        if isinstance(path, str) and path.startswith('/'):
            param = path.split('/')
            del param[0] # del ""
            if param[0] in ['bin', 'etc', 'home', 'lib', 'root', 'usr']:
                dir = self.root.find(param[0])
            
            if len(param) > 1:
                del param[0]
                self.computer.terminal.set_curr_dir(dir)
                return self.find_dir(path = param)
            
            return dir
        
        elif isinstance(path, str):
            param = path.split('/')
            dir = curr_dir.find(param[0])
            if dir.is_dir(): 
                if len(param) > 1:
                    del param[0]
                    self.computer.terminal.set_curr_dir(dir)
                    return self.find_dir(path = param)
                return dir
            print("Directory not found.")

        elif isinstance(path, list):
            param = path
            dir = curr_dir.find(param[0])
            if dir.is_dir():
                if len(param) > 1:
                    del param[0]
                    self.computer.terminal.set_curr_dir(dir)
                    return self.find_dir(path = param)
                return dir
            print("Directory not found.")

        return dir
        



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

