import os
from time import time, sleep
from datetime import datetime
from hashlib import md5
from typing import Optional, Dict, List

from .user import User, Group

class Computer:

    def __init__(self):
        self.boot_time = datetime.now()
        self.hostname: Optional[str] = None
        self.users: Dict[int, User] = {}
        self.groups: Dict[int, Group] = {}
        self.id = 1
        self.terminal = None
        self.public_ip: str
        self.local_ip: str
        