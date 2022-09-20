from enum import Enum, auto

class FileStatus(Enum):
    # Not allowed to write, read or execute
    NOT_ALLOWED = auto()
    # Can't execute because of other problems rather than permissions.
    CANNOT_EXECUTE = auto()
    # A file was expected, but a directory was given.
    IS_DIR = auto()
    # A directory was expected, but a file was given.
    IS_FILE = auto()
    # File or directory not found
    NOT_FOUND = auto()