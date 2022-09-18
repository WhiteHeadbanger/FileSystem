from lib.term import output
from lib.unistd import listdir, cat
from utils import StandardStatus

def main(filename):
    curr_dir = listdir()
    file = curr_dir.find(filename)
    response = cat(file)

    if not response.success:
        if response.error_message == StandardStatus.IS_DIR:
            return output(f"Error: {file.name} is a directory")

    return output(f"{response.data}")
    