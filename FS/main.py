from computer import Computer
from getpass import getpass

def create_user():
    while True:
        fullname = input("Full name (optional): ")
        username = input("Username: ")
        password = getpass("Password: ")
        password_confirm = getpass("Confirm password: ")
        hostname = input("Hostname: ")
        if password != password_confirm:
            print("Password do not match.")
        else:
            break
    return fullname, username, password, hostname

if __name__ == '__main__':
    from sys import path
    from os.path import dirname as dir

    path.append(dir(path[0]))
    
    fullname, username, password, hostname = create_user()
    computer = Computer()
    computer.init((username, password, hostname, fullname))
    while True:
        computer.run()