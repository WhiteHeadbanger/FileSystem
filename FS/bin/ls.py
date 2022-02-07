from lib.term import output
from lib.unistd import listdir
from utils import StandardStatus

def main(*args):
    if args:
        return output("Command not recognized.")

    current_dir = listdir()
    current_dir = current_dir.files
    output(current_dir)