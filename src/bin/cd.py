from lib.unistd import chdir
from lib.term import output

from src.status.response import StandardStatus

def main(args):
    response = chdir(args)

    if not response.success:
        return output(response)
    
    
