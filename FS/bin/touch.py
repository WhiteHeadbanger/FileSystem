from lib.unistd import touch

def parse(args):
    arg_list = args.split()
    if len(arg_list) > 1:
        filename = args[0]
        content = args[1]
        del args[0]
        del args[0]
        for arg in args:
            content = f"{content} {arg}"
        return filename, content
    filename = args
    content = ""
    return filename, content


def main(args):
    filename, content = parse(args)
    touch(filename, content)