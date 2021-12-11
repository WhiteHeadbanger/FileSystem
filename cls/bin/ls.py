from ..lib.term import listdir, output

from typing import Dict

def main(*args):
    current_dir = listdir()
    current_dir: Dict[str, object] = current_dir.files
    output(current_dir)