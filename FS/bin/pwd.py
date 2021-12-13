from lib.term import output
from lib.unistd import pwd

def main():
    path = pwd()
    output(path)