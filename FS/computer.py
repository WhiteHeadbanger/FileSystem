import os
import importlib
import uuid
from time import time, sleep
from datetime import datetime
from hashlib import md5
from typing import Optional, Dict, List, Literal, Union, Tuple

from user import User
from group import Group
from session import Session
from terminal import Terminal
from file_system import StdFS, File, Directory
from lib import unistd, term
from utils import Response, StandardStatus

class Computer:

    def __init__(self) -> None:
        self.start_time = datetime.now()
        self.hostname: Optional[str] = None
        self.users: Dict[str, User] = {}
        self.groups: Dict[str, Group] = {}
        self.sessions: List[Session] = []
        self.current_session: Session = None
        self.id = 1
        self.terminal = None
        self.fs = None
        self.public_ip: str
        self.local_ip: str
        self.env: dict = {"$PATH":None, "$HOME":None, "$CWD":None}

    def init(self, userdata: Tuple[str]) -> None:
        """ Initialize the computer """
        self.create_root()
        self.create_user((userdata[0], userdata[1], userdata[3]))
        self.set_hostname(userdata[2])
        self.set_fs()
        self.set_env_var('$PATH')
        self.set_env_var('$HOME')
        self.set_env_var('$CWD')
        user = self.get_user_by(username = userdata[0])
        self.create_session(user.uid)
        self.set_session(self.sessions[0])
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
        try:
            module = importlib.import_module(f"bin.{cmd}")
        except ModuleNotFoundError:
            print("Command not recognized")
            return
        if len(args) == 1:
            module.main(args[0])
        elif not args:
            module.main()
        else:
            module.main(args)

    def chdir(self, path: Union[str, List[str]]) -> Response:
        """ Changes current directory """

        file = self.fs.find_dir(path)
        if file.is_dir() and file is not None:
            self.current_session.curr_dir = file
            self.terminal.set_curr_dir(file)
            return Response(success = True)
        
        return Response(success = False, error_message = StandardStatus.IS_FILE)

    def mkdir(self, name: str, source) -> Response:
        """ Creates a directory """

        return Response(success = True, data = self.fs.make_dir(name, source))

    def touch(self, name: str, content: str) -> None:
        """ Creates a file """
        
        self.fs.make_file(name, content)

    def rm(self, name: str) -> None:
        """ Deletes a file or directory """
        
        self.fs.delete(name)

    def mv(self, source: str, destination: str) -> None:
        """ Moves (rename) a file """
        
        self.fs.move(source, destination)

    def cat(self, file) -> Response:
        """ Reads from file """

        try:
            file_reading = file.read()
        except AttributeError:
            return Response(success=False, error_message=StandardStatus.IS_DIR)
        
        return Response(success=True, data = file_reading)
    
    def pwd(self) -> None:
        """ Prints working directory """

        return self.fs.print_working_directory()

    def clear(self) -> None:
        """ Clear the screen """

        return self.fs.clear()

    def whoami(self) -> None:
        """ Return the logged username """

        return self.fs.whoami()

    def sudo(self, username: Optional[str] = None) -> None:
        """ Switch between registered users """

        return self.fs.sudo(username)

    def exit(self) -> None:
        """ Exits current session and returns to the previous one """

        return self.fs.exit()

    def get_start_time(self) -> datetime:
        """ Returns boot start time """

        return self.start_time

    def get_hostname(self) -> str:
        """ Returns computer's hostname """

        return self.hostname

    def get_users(self) -> Dict[str, User]:
        """ Returns all users available """
        
        return self.users

    def get_user_by(self, username: Optional[str] = None, uid: Optional[str] = None) -> Optional[User]:
        """ Returns a user by its username or uid """

        if uid:
            user = self.users.get(uid)
        elif username:
            for usr in self.users.values():
                if usr.username == username:
                    user = usr
                    break
                user = None
        else:
            user = None

        return user



    def get_groups(self) -> Dict[int, Group]:
        """ Returns all groups available """

        return self.groups

    def get_current_session(self) -> Session:
        """ Returns current session """
        
        return self.current_session

    def get_sessions(self) -> List[Session]:
        """ Returns all sessions available """

        return self.sessions

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

    def set_session(self, session: Session) -> None:
        """ Sets current shell session """

        self.current_session = session

    def get_session_by(self, uid: str) -> Session:
        """ Returns a session by id """
        
        s = None
        for sess in self.sessions:
            s = sess if sess.uid == uid else None
        return s

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

    def create_root(self) -> None:
        """ Creates the root user """

        uid = uuid.uuid4().hex
        self.users[uid] = User(uid = uid, username = "root", password = "toor", name = "root")

    def create_user(self, user) -> None:
        """ Creates a new user """

        uid = uuid.uuid4().hex
        self.users[uid] = User(uid = uid, username = user[0], password = user[1], name = user[2])

    def set_hostname(self, hostname: str) -> None:
        """ Sets the computer hostname """
        
        self.hostname = hostname

    def create_session(self, uid: str, dir: Optional[Directory] = None) -> None:
        """ Creates a shell session """

        id = uuid.uuid4().hex
        if not dir:
            return self.sessions.append(Session(id = id, uid = uid, curr_dir = self.env.get("$CWD")))
        
        self.sessions.append(Session(id = id, uid = uid, curr_dir = dir))


    def logout(self) -> None:
        """ Logs off the system """
        
        pass