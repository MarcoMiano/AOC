# AOC22 D6p1: Tuning Trouble

import os
from pprint import pprint
from dataclasses import dataclass


@dataclass()
class File(object):
    file_name: str
    size: int


class Directory(object):
    def __init__(self, dir_name) -> None:
        self._name: str = dir_name
        self._files: list[File] = []
        self._sub_dirs: list[Directory] = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def parent_dir(self) -> "Directory":
        return self._parent_dir

    @parent_dir.setter
    def parent_dir(self, p_dir: "Directory") -> None:
        self._parent_dir = p_dir

    @property
    def directories(self) -> list["Directory"]:
        return self._sub_dirs

    def add_dir(self, new_dir: "Directory"):
        self._sub_dirs.append(new_dir)
        new_dir.parent_dir = self

    def add_file(self, new_file: File):
        self._files.append(new_file)

    def get_dir(self, name: str) -> "Directory":
        return next(dir for dir in self.directories if dir.name == name)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} (name={self.name},files={self.files} dirs={self.directories})"


MAX_SIZE = 100000


def main() -> None:
    root_dir = Directory("/")
    current_dir = root_dir

    input_path = os.path.dirname(__file__) + "\\input-sm.txt"
    with open(input_path) as f:
        input_file = f.readlines()

    for line in input_file:
        tokens: list[str] = line.strip("\n").split()
        if tokens[0] == "$":
            if tokens[1] == "ls":
                continue  # skip to next line

            elif tokens[1] == "cd":  # change directory
                if tokens[2] == "..":  # go pack to parent directory
                    assert current_dir.name != "/", "Cannot go up from root"
                    current_dir = current_dir.parent_dir
                else:
                    if tokens[2] != "/":
                        current_dir = current_dir.get_dir(tokens[2])
                    else:
                        current_dir = root_dir
            else:
                assert False, f"{tokens[1]} is an invalid command"
        else:  # we are in file listing mode
            if tokens[0] == "dir":  # add a new direcotory
                current_dir.add_dir(Directory(tokens[1]))
            else:
                current_dir.add_file(File(tokens[1], size=int(tokens[0])))

    pprint(root_dir.directories)


if __name__ == "__main__":
    main()
