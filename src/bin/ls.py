from lib.term import output
from lib.unistd import listdir
#from utils import StandardStatus

def main(*args):
    if args:
        return output("Command not recognized.")

    current_dir = listdir()
    output(current_dir.files)