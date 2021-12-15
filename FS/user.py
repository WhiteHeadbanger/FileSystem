from typing import Optional, Dict

class User:
    """ Represents a user account on the system """

    def __init__(self, uid: Optional[int] = None, username: Optional[str] = None, password: Optional[str] = None, name: Optional[str] = None) -> None:
        self.uid: Optional[int] = uid
        self.username: Optional[str] = username
        self.password: Optional[str] = password
        self.name: Optional[str] = name

class Group:
    """ Represents a permission group """

    def __init__(self) -> None:
        pass