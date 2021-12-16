terminal = None

def update(computer):
    global terminal
    terminal = computer.terminal

def listdir():
    return terminal.get_curr_dir()

def output(msg):
    return terminal.output(msg)