from .computer import Computer
from .file_system import FileSystem

class Terminal:

    def __init__(self, computer: Computer) -> None:
        self.file_system: FileSystem
        self.current_directory: str