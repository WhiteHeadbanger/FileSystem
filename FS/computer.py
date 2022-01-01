import os
import importlib
from time import time, sleep
from datetime import datetime
from hashlib import md5
from typing import Optional, Dict, List, Literal, Union

from user import User, Group
from terminal import Terminal
from file_system import StdFS, File, Directory
from lib import unistd, term

class Computer:

    def __init__(self) -> None:
        self.start_time = datetime.now()
        self.hostname: Optional[str] = None
        self.users: Dict[int, User] = {}
        self.groups: Dict[int, Group] = {}
        self.session: User = None
        self.id = 1
        self.terminal = None
        self.fs = None
        self.public_ip: str
        self.local_ip: str
        self.env: dict = {"$PATH":None, "$HOME":None, "$CWD":None}

    def init(self, data) -> None:
        """ Initialize the computer """

        self.create_user((data[0], data[1]))
        self.set_hostname(data[2])
        self.set_fs()
        self.set_env_var('$PATH')
        self.set_env_var('$HOME')
        self.set_env_var('$CWD')
        self.set_terminal()
        
    def update_lib(self) -> None:
        """ To run a command there is a need to access a System Library. 
        Before the command runs, a reference is passed to the Computer object.
        This way we avoid to use the Computer object as an argument for the commands."""

        libs = [unistd, term]
        for lib in libs:
            lib.update(self)

    def run(self) -> None:
        """ Runs the terminal """

        self.terminal.run()

    def run_command(self, cmd: str, args: Union[str, List[str], None]) -> None:
        """ Executes the built-in command's code"""

        self.update_lib()
        module = importlib.import_module(f"bin.{cmd}")
        if len(args) == 1:
            module.main(args[0])
        elif not args:
            module.main()
        else:
            module.main(args)

    def chdir(self, path: Union[str, List[str]]) -> None:
        """ Changes current directory """

        file = self.fs.find_dir(path)
        if file.is_dir() and file is not None:
            self.terminal.set_curr_dir(file)
            #self.terminal.curr_dir = f"/{file}"
        # return Response(msg = "Error: path not recognizable")

    def mkdir(self, name: str) -> None:
        """ Creates a directory """

        self.fs.make_dir(name)

    def touch(self, name: str, content: str) -> None:
        """ Creates a file """
        
        self.fs.make_file(name, content)

    def rm(self, name: str) -> None:
        """ Deletes a file or directory """
        
        self.fs.delete(name)

    def mv(self, source: str, destination: str) -> None:
        """ Moves (rename) a file """
        
        self.fs.move(source, destination)
    
    def pwd(self) -> None:
        """ Prints working directory """

        return self.fs.print_working_directory()

    def cls(self) -> None:
        """ Clear the screen """

        return self.fs.clear_screen()

    def get_start_time(self) -> datetime:
        """ Returns boot start time """

        return self.start_time

    def get_hostname(self) -> str:
        """ Returns computer's hostname """

        return self.hostname

    def get_users(self) -> Dict[int, User]:
        """ Returns all users available """
        
        return self.users

    def get_groups(self) -> Dict[int, Group]:
        """ Returns all groups available """

        return self.groups

    def get_session(self) -> User:
        """ Returns current session """
        
        return self.session

    def get_terminal(self) -> Terminal:
        """ Returns the terminal """
        
        return self.terminal

    def get_public_ip(self) -> str:
        """ Returns the public IP """
        
        return self.public_ip

    def get_local_ip(self) -> str:
        """ Returns the local IP """
        
        return self.local_ip

    def set_terminal(self) -> None:
        """ Creates the terminal """
        
        self.terminal: Terminal = Terminal(self)

    def set_fs(self) -> None:
        """ Creates the file system """
        
        self.fs: StdFS = StdFS(self)

    def set_env_var(self, var: str, value: str = None) -> None:
        """ Sets environment variable """
        
        default_env_var = {"$PATH":["/bin"], "$HOME":f"/home", "$CWD":self.fs.get_root()}
        if not value:
            self.env[var] = default_env_var[var]
            return
        self.env[var] = value        

    def get_env_var(self, var) -> Union[List, str, Directory]:
        """ Returns a environment variable """
        
        return self.env[var]

    def create_user(self, user) -> None:
        """ Creates a new user """
        
        self.session = User(username = user[0], password = user[1])

    def set_hostname(self, hostname: str) -> None:
        """ Sets the computer hostname """
        
        self.hostname = hostname

    def logout(self) -> None:
        """ Logs off the system """
        
        pass