from lib.term import output
from lib.unistd import listdir
#from utils import StandardStatus

def main():
    current_dir = listdir()
    output(current_dir.files)