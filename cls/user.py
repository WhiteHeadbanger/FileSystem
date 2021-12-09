from typing import Optional

class User:

    def __init__(self, uid: Optional[int] = None, username: Optional[str] = None, password: Optional[str] = None, name: Optional[str] = None):
        self.uid: Optional[int] = uid
        self.username: Optional[str] = username
        self.password: Optional[str] = password
        self.name: Optional[str] = name