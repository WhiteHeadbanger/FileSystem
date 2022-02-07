from lib.unistd import chdir
from lib.term import output
from utils import StandardStatus

def main(args):
    response = chdir(args)

    if not response.success:
        if response.error_message == StandardStatus.IS_FILE:
            return output(f"Error: {args} is a file.")
    
    
