# Virtual File System  

This is a simple virtual file system inspired by Linux.
GUI is not functional, but usable. You can delete the entire folder if you want.

## Available commands

* `whoami` (returns the username)
* `touch <filename> <content>` (creates a file with a content, like a txt file)
* `sudo root` (password: toor) (currently does nothing else besides changing the current user session)
* `rm <filename>` (deletes a file)(only inside the current directory, for now)
* `pwd` (prints working directory)
* `mv <source file | dir> <destination dir>` (moves a file or directory)
* `mkdir <dirname>` (creates a directory)
* `ls` (lists files and directories from current directory)
* `exit` (If you are on root session, it goes back to your previous session)
* `clear` (cleans your screen)
* `cd <dir | fullpath>` (changes directory)
* `cat <filename>` (reads content of a file)

## How to execute

1. Clone the project.
2. Open a terminal in FS directory
3. Type `python3 main.py`
4. Beware, it's buggy.

## Next steps in the project

* More commands.
* Refactor, because the code is awful.
* Eventually work on the GUI.
* Maaaaybe implement some kind of bash language, or an entirely new language to create scripts.



