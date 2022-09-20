from enum import Enum, auto

class StandardStatus(Enum):
    # General error code. It can be triggered by anything that doesn't belong to the other error codes.
    GENERIC_ERROR = auto()

    def __str__(self):
        return self.name