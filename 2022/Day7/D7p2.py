# AOC22 D7p2: No Space Left On Device
# My adaptation of https://aoc.just2good.co.uk/2022/7

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

    @property
    def files(self) -> list[File]:
        return self._files

    @property
    def size(self) -> int:
        return sum(file.size for file in self._files) + sum(
            sub_dir.size for sub_dir in self._sub_dirs
        )

    def add_dir(self, new_dir: "Directory"):
        self._sub_dirs.append(new_dir)
        new_dir.parent_dir = self

    def add_file(self, new_file: File):
        self._files.append(new_file)

    def get_dir(self, name: str) -> "Directory":
        return next(dir for dir in self.directories if dir.name == name)

    def get_all_dirs(self) -> list["Directory"]:
        all_dirs = []
        for directory in self.directories:
            all_dirs.extend(directory.get_all_dirs())

        all_dirs.extend(self.directories)
        return all_dirs

    def _print(self, iteration: int) -> str:
        def tab(n):
            return n * "\t"

        result = (
            tab(iteration)
            + f"{self.__class__.__name__}\n{tab(iteration + 1)}"
            + f"name={self.name}\n{tab(iteration + 1)}"
            + f"size={self.size}\n{tab(iteration + 1)}"
            + f"sub_dirs="
            + (f"\n" if self._sub_dirs else f"NONE\n")
        )

        for sub_dir in self._sub_dirs:
            result += tab(iteration + 1) + sub_dir._print(iteration=iteration + 1)
        return result

    def __repr__(self) -> str:
        return self._print(0)


def file_parse(input_file: list[str]) -> Directory:
    root_dir = Directory("/")
    current_dir = root_dir

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

    return root_dir


DISK_CAPACITY = 70_000_000
REQUIRED_FREE_SPACE = 30_000_000


def main() -> None:
    input_path = os.path.dirname(__file__) + "\\input.txt"
    with open(input_path) as f:
        input_file = f.readlines()

    root_dir = file_parse(input_file)

    free_space = DISK_CAPACITY - root_dir.size
    print(free_space)
    possible_dirs: list[Directory] = [
        directory
        for directory in root_dir.get_all_dirs()
        if directory.size >= REQUIRED_FREE_SPACE - free_space
    ]
    print(min(possible_dirs, key=lambda x: x.size).size)


if __name__ == "__main__":
    main()
