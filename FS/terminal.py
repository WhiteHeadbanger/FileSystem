from file_system import StdFS


class Terminal:

    def __init__(self, computer: object) -> None:
        self.computer = computer
        self.fs = computer.fs
        self.rootdir  = computer.env.get("$CWD")
        self.curr_dir = self.rootdir.find('home').find(self.computer.session.username)
        self.path: list = computer.env.get("$PATH")

        self.outbox = []
        self.complete_outbox = []

    def get_curr_dir(self):
        return self.curr_dir

    def set_curr_dir(self, dir):
        self.curr_dir = dir

    def get_path(self):
        return self.path

    def parse_raw(self, cmd: str):
        """ Handles and parses the raw input"""

        command = cmd.split()
        command_name = command[0]
        # Use "del" because we already have the command name, so we don't need to return it (as oppose to "command.pop(0)")
        del command[0]
        args = command
        self.computer.run_command(command_name, args)
        return (command_name, args)

    def output(self, msg):
        if isinstance(msg, dict):
            for files in msg.keys():
                print(files)
        else:
            print(msg)

    def input(self):
        cmd = None
        while cmd is None:
            cmd = input(f"{self.computer.session.username}@{self.computer.hostname}#/{self.curr_dir.name}:> ")
            parsed_cmd: tuple = self.parse_raw(cmd)
        
        return parsed_cmd

    def run(self):
        self.running = True
        msg = "Hello"
        self.output(msg)
        while self.running:
            self.input()
            
            