from dataclasses import dataclass, field
from typing import List, Optional, Union, Dict


@dataclass
class OS:
    """
    shells: List['id'] = current open shells
    current_directory_shells: Dict['id':'current_directory'] = current open shells with it's current directory
    terminals: int = current open terminals
    """
    shells: List[str] = field(default_factory=list)
    current_directory_shells: Dict[str, str] = field(default_factory=dict)
    terminals: int = field(default=1)

    def add_shell(self, id: str) -> None:
        """ Adds a new shell to the list """

        self.shells.append(id)

    def remove_shell(self, id: str) -> None:
        """ Removes a shell from the list and the current_directory_shells dict """

        if id not in self.shells:
            return False
        self.shells.remove(id)
        del self.current_directory_shells[id]
    
    def chg_curr_dir(self, id: str, dir: str) -> None:
        """ Changes the current directory of a given shell id """

        if id not in self.shells:
            return False
        self.current_directory_shells[id] = dir

    
            