from lib.term import output
from lib.unistd import listdir, cat

def main(filename):
    curr_dir = listdir()
    file = curr_dir.find(filename)
    response = cat(file)

    if not response.success:
        return output(response)

    return output(f"{response.data}")
    