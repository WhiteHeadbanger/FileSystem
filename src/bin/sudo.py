from lib.unistd import sudo

def main(*args):
    if args:
        sudo(args[0])
    return