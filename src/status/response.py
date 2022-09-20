from typing import Optional, Any, Callable, Union
from status.standard_status import StandardStatus
from status.file_status import FileStatus
from status.session_status import SessionStatus
from status.command_status import CommandStatus

import json, os

__THIS_FOLDER__ = os.path.dirname(__file__)

status_list = [StandardStatus, FileStatus, SessionStatus, CommandStatus]

def load_json():
    data = None
    with open(os.path.join(__THIS_FOLDER__, 'error_status.json'), 'r') as f:
        data = json.load(f)
    return data

class Response:
    """ Standarize response objects """

    __text__ = load_json()

    def __init__(self, success: bool, error_message: Optional[Union[StandardStatus, FileStatus, SessionStatus, CommandStatus]] = None, data: Any = None, func: Optional[Callable] = None, **kwargs) -> None:
        """ 
        success: whether or not the response succeded.
        error_message: the error message.
        data: data to be returned
        exec: if set to true, data can contain a callable and use kwargs to pass them to the function.
        """

        self.success = success
        self.error_message = error_message
        self.data = data
        self.func = func
        if func:
            self.execute(**kwargs)

    def __str__(self) -> str:
        for class_name in status_list:
            if isinstance(self.error_message, class_name):
                status_name = Response.__text__[class_name]
        
        for status_data in Response.__text__[status_name]:
            if status_data["name"] == self.error_message.name:
                txt = status_data["str"]

        return txt

    def execute(self, **kwargs):
        return self.func(**kwargs)

