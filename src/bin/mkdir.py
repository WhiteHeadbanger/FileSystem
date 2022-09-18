from lib.unistd import mkdir, listdir

def main(filename):
    current_directory = listdir()
    mkdir(filename, current_directory)