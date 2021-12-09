import os
from time import time, sleep
from datetime import datetime
from hashlib import md5
from typing import Optional, Dict, List, Literal

from .user import User, Group

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
        self.env = {"$PATH":None, "$HOME":None, "$PWD":f"/home/{self.session.username}"}

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

    def get_env_var(self, var):
        return self.env[var]

    def change_session(self):
        pass

    def logout(self):
        pass