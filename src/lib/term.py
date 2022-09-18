terminal = None

def update(computer):
    global terminal
    terminal = computer.terminal

def output(msg):
    return terminal.output(msg)