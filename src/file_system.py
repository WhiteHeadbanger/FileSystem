from __future__ import annotations
from typing import Optional, Dict, List, Union

import sys, os

from getpass import getpass
from status.response import Response
from status.standard_status import StandardStatus


__THIS_FOLDER__ = os.path.dirname(__file__)
__BIN__ = os.path.join(__THIS_FOLDER__, 'bin')
__LIB__ = os.path.join(__THIS_FOLDER__, 'lib')
__ROOT__ = os.path.join(__THIS_FOLDER__, 'root')
__USR__ = os.path.join(__THIS_FOLDER__, 'usr')

class FileSystem:

    def __init__(self, name: str, parent: Optional[Directory], owner: int, group_owner: int) -> None:
        self.name: str = name
        self.parent = parent
        self.owner = owner
        self.group_owner = group_owner
        self.permissions: Dict[str, str] = {}
        self.size: int

    def is_dir(self) -> bool:
        """ Return true if file is a directory """

        return type(self) == Directory

    def is_file(self) -> bool:
        """ Return true if file is a file """

        return type(self) == File

    def get_name(self) -> str:
        """ Return file name """

        return self.name

    def get_group_owner(self) -> int:
        """ Return file group owner """

        return self.group_owner

    def get_permissions(self) -> Dict:
        """ Return file permissions """

        return self.permissions

    def get_size(self) -> int:
        """ Return file size """
        return self.size

    def get_parent(self) -> Optional["Directory"]:
        """ Return file parent """
        
        return self.parent if self.name != '/' else None 

class Directory(FileSystem):

    def __init__(self, name, parent, owner, group_owner) -> None:
        super().__init__(name, parent, owner, group_owner)
        self.files = {}
        self.size = None

    def add_file(self, file: Directory | File) -> None:
        """ Add a file or directory to child files """

        if file.name not in self.files.keys():
            self.files[file.name] = file

    def find(self, filename: str) -> Union["Directory", "File", None]:
        """ Returns a child file or directory """

        if filename.startswith('/'):
            file = filename.split('/')
            del file[0] # erases '/'
            return self.files.get(file[0], None)
        
        return self.files.get(filename, None)

class File(FileSystem):

    def __init__(self, name: str, content: str, parent: Optional[Directory], owner: int, group_owner: int) -> None:
        super().__init__(name, parent, owner, group_owner)
        self.content = content
        self.size = sys.getsizeof(self.name + self.content)

    def read(self) -> str:
        """ Displays content from a file """

        return self.content

class StdFS:

    def __init__(self, computer: object) -> None:
        self.computer = computer
        self.root = Directory("/", None, 0, 0)

        self.initialize()

    def initialize(self) -> None:
        """ Creates root directories and initializes them """

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

    def get_root(self) -> Directory:
        return self.root

    def make_dir(self, name: str, source: Directory) -> None:
        """ Creates a directory in the local path """
        #TODO make absolute path too.

        dir = Directory(name, source, 0, 0)
        source.add_file(dir)

    def make_file(self, name: str, content: str) -> None:
        """ Creates a file in the local path """
        #TODO make absolute path too.

        curr_dir = self.computer.current_session.get_curr_dir()

        file = File(name, content, curr_dir, 0, 0)
        curr_dir.add_file(file)

    def delete(self, name: str, curr_dir: Directory = None) -> None:
        """ Deletes a directory or file.  """
        #TODO: make absolute path

        if curr_dir is None:
            curr_dir = self.computer.current_session.get_curr_dir()

        file_to_remove = curr_dir.find(name)
        if file_to_remove is None:
            return

        elif file_to_remove.is_file():
            file_to_remove.parent = None
            del curr_dir.files[name]
            return
            
        childs_of_file = file_to_remove.files.copy()
        if not childs_of_file:
            del curr_dir.files[name]
            return

        # Loop through file_to_remove child files
        for _, f in childs_of_file.items():
            if f.is_dir():
                if not f.files:
                    f.parent = None
                    del file_to_remove.files[f.name]
                    continue
            del file_to_remove.files[f.name]

        del curr_dir.files[name]

    
    def move(self, source: str, dest: str) -> None:
        """ Moves a file or directory """

        src = self.find_dir(source)
        dst = self.find_dir(dest)
        current_dir = self.computer.current_session.get_curr_dir()

        if src is None:
            return Response(success = False, error_message = StandardStatus.NOT_FOUND, data = src)
        
        # If we want to rename a file
        elif dst is None:
            src_parent = src.get_parent()
            if src_parent is None:
                src_parent = self.root
            src_parent.files[dest] = src_parent.files.pop(src.name)
            src.name = dest
            return Response(success = True)
        
        if dst.is_dir():
            src_parent = src.get_parent()
            src.parent = dst
            dst.add_file(src)
            del current_dir.files[src.name]
            return Response(success = True)

        return Response(success = False, error_message = StandardStatus.GENERIC_ERROR)

        
    def print_working_directory(self, abspath: List = [], curr_dir: Directory = None) -> str:
        """ Outputs absolute working directory """
        
        if curr_dir is None:
            curr_dir = self.computer.terminal.get_curr_dir()
            abspath = []
        
        if curr_dir.name == '/':
            if not abspath:
                return '/'
            abspath.reverse()
            abspath = "".join(abspath)
            return abspath        

        abspath.append(curr_dir.name)
        abspath.append('/')

        parent = curr_dir.get_parent()
        
        while parent:
            return self.print_working_directory(abspath = abspath, curr_dir = parent)

    def clear(self) -> None:
        """ Clear screen """

        # Windows
        if os.name == 'nt':
            os.system('cls')
        else:
            #Linux and mac
            os.system('clear')

    def whoami(self) -> None:
        """ Return the logged username """

        sess_uid = self.computer.current_session.uid
        return self.computer.get_user_by(uid = sess_uid).username

    def sudo(self, user_name: Optional[str] = None) -> None:
        """ Switch between registered users """

        if not user_name:
            return
        
        current_userid = self.computer.current_session.uid
        current_user = self.computer.get_user_by(uid = current_userid)
        
        # Check if username is the current session username
        if user_name == current_user.username:
            return

        # Check if user exists on the computer
        user = self.computer.get_user_by(username = user_name)
        if user is None:
            return print("Username does not exist.")

        # Check if user session already exists
        """ for session in self.computer.sessions:
            if session.uid == user.uid:
                password = getpass("Password: ")
                if password != user.password:
                    return print("Wrong password.")
                self.computer.set_session(session)
                self.computer.terminal.set_curr_dir(session.curr_dir)
                return """

        # If session already exists, encourage to use "exit" command to return.
        for session in self.computer.sessions:
            if session.uid == user.uid:
                print("Use <exit> command to return to the previous session.")
                return
        
        # Check if passwords matches. If not, return
        password = getpass("Password: ")
        if password != user.password:
            return print("Wrong password.")

        # If user session does not exists, create it and set it as new session
        self.computer.create_session(user.uid)
        sessions = self.computer.get_sessions()
        sess = sessions[-1]
        self.computer.set_session(sess)
        self.computer.terminal.set_curr_dir(sess.curr_dir)

    def exit(self) -> None:
        """ Exits current session and returns to the previous one. 
        This command erases the current open shell """

        # Check if there's a previous open shell
        try: previous_session = self.computer.sessions[-2]
        except IndexError: return

        self.computer.set_session(previous_session)
        self.computer.terminal.set_curr_dir(previous_session.curr_dir)

        del self.computer.sessions[-1]

        

    def init_bin(self) -> None:
        """ Initializes /bin directory """

        bin_dir = self.root.find('bin')
        files = os.listdir(__BIN__)
        for file in files:
            if file not in ['__init__.py', '__pycache__', '.vscode']:
                bin_file = File(file.replace(".py", ""), "Cannot read binary data.", bin_dir, 0, 0)
                bin_dir.add_file(bin_file)
    
    def init_home(self) -> None:
        """ initializes /home directory """

        home_dir = self.root.find('home')

        for usr in self.computer.users.values():
            username = usr.username if usr.username != "root" else None
        user: Directory = Directory(username, home_dir, 0, 0)

        home_dir.add_file(user)

        def init_user() -> None:
            folders = ['Desktop', 'Downloads', 'Pictures', 'Music']
            for folder in folders:
                d: Directory = Directory(folder, user, 0, 0)
                user.add_file(d)  

        return init_user()

    def find_dir(self, path: Union[str, List[str]], curr_dir: Directory = None) -> Union[Directory, File]:
        """ 
        Finds a specific directory of file within the file system
        returns: Directory | File
        """

        # Current directory
        if curr_dir is None:
            curr_dir = self.computer.terminal.get_curr_dir()

        # If path is referencing /, return root directory (not '/root')
        if path == '/':
            return self.root

        # Return parent if exists, otherwise return root (TODO: standarize response messages)
        if path == '..':
            parent_dir = curr_dir.get_parent()
            if parent_dir is not None:
                return parent_dir
            return self.root

        if isinstance(path, str) and path.startswith('/'):
            param = path.split('/')
            del param[0] # del ""
            if param[0] in ['bin', 'etc', 'home', 'lib', 'root', 'usr']:
                dir = self.root.find(param[0])
            
            if len(param) > 1:
                dir = param[0]
                del param[0]
                return self.find_dir(path = param, curr_dir = curr_dir.find(dir))
            
            return self.find_dir(path = param[0])

        elif isinstance(path, str):
            param = path.split('/')

        elif isinstance(path, list):
            param = path
        
        dir = curr_dir.find(param[0])
        if dir is not None:
            if dir.is_dir(): 
                if len(param) > 1:
                    del param[0]
                    return self.find_dir(path = param, curr_dir = dir)
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

