from file_system import StdFS, Directory
from typing import Optional


class Terminal:

    def __init__(self, computer: object) -> None:
        self.computer = computer
        self.fs = computer.fs
        #self.rootdir  = computer.env.get("$CWD")
        sess_uid = computer.current_session.uid
        self.curr_dir = computer.current_session.curr_dir.find('home').find(self.computer.get_user_by(uid = sess_uid).username)
        computer.current_session.curr_dir = self.curr_dir
        self.path: list = computer.env.get("$PATH")

        self.outbox = []
        self.complete_outbox = []

    def get_curr_dir(self) -> Directory:
        """ Return current directory """

        return self.curr_dir

    def set_curr_dir(self, dir: Directory) -> None:
        """ Sets current directory """
        
        self.curr_dir = dir

    def get_path(self) -> list:
        """ Returns a list of directories from which the system will look to execute commands """
        
        return self.path

    def parse_raw(self, cmd: str) -> None:
        """ Handles and parses raw input"""

        command = cmd.split()
        command_name = command[0]
        # Using "del" because we already have the command name, so we don't need to return it (as oppose to "command.pop(0)")
        del command[0]
        args = command
        self.computer.run_command(command_name, args)

    def output(self, msg) -> None:
        """ Outputs on the screen """

        if isinstance(msg, dict):
            for files in msg.keys():
                print(files)
        else:
            print(msg)

    def input(self) -> None:
        """ Command input """

        cmd = None
        sess_uid = self.computer.get_current_session().uid
        while cmd is None:
            cmd = input(f"{self.computer.get_user_by(uid = sess_uid).username}@{self.computer.hostname}#/{self.curr_dir.name}:> ")
            if cmd:
                self.parse_raw(cmd)

    def run(self) -> None:
        """ Input loop """

        self.running = True
        while self.running:
            self.input()
            
            