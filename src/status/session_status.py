from enum import Enum, auto

class SessionStatus(Enum):
     # Username not found
    USER_NOT_FOUND = auto()
    # Current session is username
    USER_IN_CURRENT_SESSION = auto()
    # Session is already created
    USER_SESSION_ALREADY_EXISTS = auto()
    # Wrong password
    WRONG_PASSWORD = auto()