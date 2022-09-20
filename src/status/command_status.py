from enum import Enum, auto

class CommandStatus(Enum):
    # Command isn't found on the system.
    COMMAND_NOT_FOUND = auto()
    # Invalid argument pass to the command
    INVALID_ARGUMENT = auto()