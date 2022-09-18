from typing import List, Union, Optional

class Group:
    """ Represents a permission group """

    def __init__(self, id: int, name: str, description: Optional[str], uid: Union[List[int], None] = None) -> None:
        """
        id: Group's id
        name: Group's name
        description: Group's description
        uid: Group's list of user id's
        """
        self.id = id
        self.name = name
        self.description = description
        self.uid = uid