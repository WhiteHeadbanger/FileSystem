from lib.unistd import mv

def main(args) -> None:
    mv(args[0], args[1])