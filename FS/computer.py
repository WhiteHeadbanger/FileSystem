import os
import importlib
from time import time, sleep
from datetime import datetime
from hashlib import md5
from typing import Optional, Dict, List, Literal, Union

from user import User, Group
from terminal import Terminal
from file_system import StdFS
from lib import unistd, term

class Computer:

    def __init__(self):
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

    def init(self, data):
        self.create_user((data[0], data[1]))
        self.set_hostname(data[2])
        self.set_fs()
        self.set_env_var('$PATH')
        self.set_env_var('$HOME')
        self.set_env_var('$CWD')
        self.set_terminal()
        
    def update_lib(self):
        """ To run a command there is a need to access a System Library. 
        Before the command runs, a reference is passed to the Computer object.
        This way we avoid to use the Computer object as an argument for the commands."""

        libs = [unistd, term]
        for lib in libs:
            lib.update(self)

    def run(self):
        self.terminal.run()

    def run_command(self, cmd: str, args: Union[str, List[str], None]):

        self.update_lib()
        module = importlib.import_module(f"bin.{cmd}")
        if len(args) == 1:
            module.main(args[0])
        elif not args:
            module.main()
        else:
            module.main(args)

    def chdir(self, path: Union[str, List[str]]):
        """ Changes current directory """

        file = self.fs.find_dir(path)
        self.terminal.set_curr_dir(file)
        #self.terminal.curr_dir = f"/{file}"

    def mkdir(self, name: str):
        self.fs.make_dir(name)

    def touch(self, name: str, content: str):
        self.fs.make_file(name, content)

    def rm(self, name: str):
        self.fs.delete(name)
    
    def get_start_time(self):
        return self.start_time

    def get_hostname(self):
        return self.hostname

    def get_users(self):
        return self.users

    def get_groups(self):
        return self.groups

    def get_session(self):
        return self.session

    def get_terminal(self):
        return self.terminal

    def get_public_ip(self):
        return self.public_ip

    def get_local_ip(self):
        return self.local_ip

    def set_terminal(self):
        self.terminal: Terminal = Terminal(self)

    def set_fs(self):
        self.fs: StdFS = StdFS(self)

    def set_env_var(self, var: str, value: str = None):
        default_env_var = {"$PATH":["/bin"], "$HOME":f"/home", "$CWD":self.fs.get_root()}
        if not value:
            self.env[var] = default_env_var[var]
            return
        self.env[var] = value        

    def get_env_var(self, var):
        return self.env[var]

    def get_current_directory(self):
        return self.fs.get_root()


    def create_user(self, user):
        self.session = User(username = user[0], password = user[1])

    def set_hostname(self, hostname: str):
        self.hostname = hostname

    def change_session(self):
        pass

    def logout(self):
        pass