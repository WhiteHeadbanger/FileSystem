from enum import Enum, auto
from typing import Optional, Any

class StandardStatus(Enum):
    """ Standarize status codes """
    
    # General error code. It can be triggered by anything that doesn't belong to the next error codes.
    GENERIC_ERROR = auto()
    # Not allowed to write, read or execute
    NOT_ALLOWED = auto()
    # Can't execute because of other problems rather than permissions.
    CANNOT_EXECUTE = auto()
    # Command isn't found on the system.
    COMMAND_NOT_FOUND = auto()
    # Invalid argument pass to the command
    INVALID_ARGUMENT = auto()
    # A file was expected, but a directory was given.
    IS_DIR = auto()
    # A directory was expected, but a file was given.
    IS_FILE = auto()


class Response:
    """ Standarize response objects """

    def __init__(self, success: bool, error_message: Optional[StandardStatus] = None, data: Any = None, exec = False, **kwargs) -> None:
        """ 
        success: whether or not the response succeded.
        error_message: the error message.
        data: data to be returned
        exec: if set to true, data can contain a callable and use kwargs to pass them to the function.
        """

        self.success = success
        self.error_message = error_message
        self.data = data
        self.exec = exec
        if exec:
            self.execute(kwargs)

    def __str__(self) -> str:
        return f"Error: {self.error_message}, data: {self.data}"

    def execute(self, kwargs):
        return self.data(kwargs)

