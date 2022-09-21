# Virtual File System  

This is a simple virtual file system inspired by Linux. This is just one of my hobbie projects, I don't make money with it. Since I was a child I wanted to create my own OS, and this is the closest I can be with that idea.
GUI is not functional, but usable. You can delete the entire folder if you want, it will not affect the functionality of the file system.

## How to execute

1. Clone the project.
2. Open a terminal in 'src' directory
3. Type `python3 main.py`
4. Beware, it's buggy.

## Available commands

* `whoami` (returns the username)
* `touch <filename> <content>` (creates a file with a content, like a txt file)
* `sudo root` (password: toor) (currently does nothing else besides changing the current user session)
* `rm <filename>` (deletes a file)
* `pwd` (prints working directory)
* `mv <source file | dir> <destination dir>` (moves a file or directory)
* `mv <source file | dir> <filename>` (renames a file or directory. Make sure the filename != dirname in current directory, otherwise it will MOVE)
* `mkdir <dirname>` (creates a directory)
* `ls` (lists files and directories from current directory)
* `exit` (If you are on root session, it goes back to your previous session)
* `clear` (cleans your screen)
* `cd <dir | fullpath>` (changes directory)
* `cat <filename>` (reads content of a file)

## Next steps in the project

* More commands. (*)
* Refactor, because the code is awful.
* Maybe, eventually, work on the GUI.
* Maaaaybe implement some kind of bash language, or an entirely new language to create scripts.

(*) Planned commands are: man, chmod, sudo (expand its current functionalities)

## How to contribute

If you feel like adding a new feature, or improving the code to make it more clean, or fixing some bug, you are very welcome! Please follow this steps:

1. Fork the repo
2. Create a branch from `main`, and name it under type/name where type is:
- feature
- refactor
- bugfix
- documentation
3. Make a pull request


