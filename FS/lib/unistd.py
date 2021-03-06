computer = None

def update(comp):
    global computer
    computer = comp

def gethostname():
    """ Returns the computer's hostname"""

    return computer.get_hostname()

def boottime():
    """ Returns the boot start time"""

    return computer.get_start_time()

def getusers():
    """ Returns a list of users """

    return computer.get_users()

def getgroups():
    """ Returns a list of groups """

    return computer.get_groups()

def getsession():
    """ Returns a session object"""

    return computer.get_session()

def getterminal():
    """ Returns a list of terminals currently opened"""

    return computer.get_terminal()

def getpublicip():
    """ Returns the public IP """

    return computer.get_public_ip()

def getlocalip():
    """ Returns the local ip"""

    return computer.get_local_ip()

def chdir(path: str):
    """ Changes terminal current directory """

    return computer.chdir(path)

def mkdir(dirname: str, source):
    """ Creates a directory"""

    return computer.mkdir(dirname, source)

def touch(filename: str, content: str):
    """ Creates a file """

    return computer.touch(filename, content)

def rm(filename: str):
    """ Deletes a directory/file """

    return computer.rm(filename)

def mv(source: str, destination: str):
    """ Moves (rename) a file """

    return computer.mv(source, destination)

def pwd():
    """ Output absolute working directory """

    return computer.pwd()

def clear():
    """ Clear the screen """

    return computer.clear()

def whoami():
    """ Return the logged username """

    return computer.whoami()

def sudo(username: str = None):
    """ Switch between registered users """

    return computer.sudo(username)

def exit():
    """ Exits current session and returns to the previous one """

    return computer.exit()

def listdir():
    """ Return current directory """

    return computer.current_session.get_curr_dir()

def cat(file):
    """ Reads from file """

    return computer.cat(file)
