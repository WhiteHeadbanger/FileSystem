from typing import Optional, Dict

class User:
    """ Represents a user account on the system """

    def __init__(self, uid: Optional[int] = None, username: str = None, password: Optional[str] = None, fullname: Optional[str] = None) -> None:
        self.uid = uid
        self.username = username
        self.password = password
        self.name = fullname

    def get_uid(self):
        """ Returns user identification """

        return self.uid

    def get_username(self):
        """ Returns username """

        return self.username

    def get_password(self):
        """ Returns password """

        return self.password

    def get_fullname(self):
        """ Returns fullname """

        return self.fullname

