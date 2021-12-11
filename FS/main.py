from computer import Computer

def main():
    username = input("Username: ")
    password = input("Password: ")
    hostname = input("Hostname: ")
    return username, password, hostname

if __name__ == '__main__':
    from sys import path
    from os.path import dirname as dir

    path.append(dir(path[0]))
    
    username, password, hostname = main()
    computer = Computer()
    computer.init((username, password, hostname))
    while True:
        computer.run()