from lib.term import listdir, output

def parse(args):
    
    if isinstance(args, str):
        arg = args.replace(".py", "")

def main(filename):
    #arg = parse(filename)
    filename = filename.replace(".py", "")
    curr_dir = listdir()
    file = curr_dir.find(filename)
    output(file.read())