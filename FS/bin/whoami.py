from lib.unistd import whoami
from lib.term import output

def main():
    user = whoami()
    output(user)