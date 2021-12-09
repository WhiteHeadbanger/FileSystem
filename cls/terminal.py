from .computer import Computer
from .file_system import StdFS
from utils import Parser

class Terminal:

    def __init__(self, computer: Computer) -> None:
        self.computer = computer
        self.fs = computer.fs
        self.curr_dir: str = computer.env["$PWD"]
        self.path: list = computer.env["$PATH"]
        self.abs_curr_dir: str = f"/root" + self.curr_dir

        self.outbox = []
        self.complete_outbox = []

    def output(self, msg):
        self.outbox.append(msg)
        self.complete_outbox.append(msg)
        if len(self.outbox) > 10:
            pass

        print(msg)

    def input(self):
        cmd = None
        while cmd == None:
            cmd = input(f"{self.computer.session.username}@{self.computer.hostname}/{self.curr_dir}/:> ") if self.curr_dir != "/" else input(f"{self.computer.session.username}@{self.computer.hostname}/:> ")
        parsed = Parser(cmd, self.path)