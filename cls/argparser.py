class Parser:

    def __init__(self, cmd, path, fs):
        self.cmd = cmd
        self.fs = fs
        self.f = self.parse(path)

    def parse(self, path):
        params = [arg for arg in self.cmd.split().split('/')]
        root = self.fs.return_root()
        for p in path:
            directory = root.find(p)
            if directory is not None:
                file = directory.find(params[0])
                if file is not None:
                    params.pop(0)
                    self.cmd = params
                    #self.execute(file)
                    return
        
        print("Command not recognized")
        return False

    #def execute(self, file):
        #exec(file.content, __globals = {"path":self.cmd})