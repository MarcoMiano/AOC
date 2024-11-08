# AOC22 D6p1: Tuning Trouble

import os
from pprint import pprint
from dataclasses import dataclass


@dataclass()
class File(object):
    file_name: str
    size: int
    directory_key: str


@dataclass()
class Directory(object):
    dir_name: str
    size: int
    file_names: list[str]
    sub_direcotories: list[str]


@dataclass()
class FileSystem(object):
    directory_tab: dict[str, Directory]
    file_tab: dict[str, File]


def calc_dir_sizes(fs: FileSystem):
    todo: list[str] = ["/"]

    while fs.directory_tab["/"].size == 0:
        d = todo[-1]

        sub_directories: list[tuple[str, int]] = [
            (sd, fs.directory_tab[sd].size)
            for sd in fs.directory_tab[d].sub_direcotories
        ]

        sub_dir_sizes: list[int] = [
            fs.directory_tab[sd].size for sd, _ in sub_directories
        ]

        if not sub_directories or all(sub_dir_sizes):
            size = 0
            for file in fs.directory_tab[d].file_names:
                size += fs.file_tab[file].size
            for _, sd_size in sub_directories:
                if sd_size == -1:
                    continue
                size += sd_size
            if size == 0:
                size = -1

            fs.directory_tab[d].size = size
            todo.pop()

        else:
            for sd, sd_size in sub_directories:
                if sd_size == 0:
                    todo.append(sd)
                    break


def main() -> None:
    filesystem = FileSystem({}, {})
    filesystem.directory_tab["/"] = Directory("/", 0, [], [])
    pwd: list[str] = list()

    input_path = os.path.dirname(__file__) + "\\input.txt"
    with open(input_path) as f:
        input_file = f.readlines()

    for line in input_file:
        tokens: list[str] = line.strip("\n").split()
        if tokens[0] == "$":
            if tokens[1] == "cd":
                if tokens[2] == "..":
                    pwd.pop()
                else:
                    pwd.append(tokens[2])
            elif tokens[1] == "ls":
                continue
        elif tokens[0] == "dir":
            if tokens[1] in filesystem.directory_tab.keys():
                continue
            filesystem.directory_tab[tokens[1]] = Directory(tokens[1], 0, [], [])
            filesystem.directory_tab[pwd[-1]].sub_direcotories.append(tokens[1])
        elif tokens[0].isdigit():
            if tokens[1] in filesystem.file_tab.keys():
                continue
            filesystem.file_tab[tokens[1]] = File(tokens[1], int(tokens[0]), pwd[-1])
            filesystem.directory_tab[pwd[-1]].file_names.append(tokens[1])

    for d in list(filesystem.directory_tab.keys()):
        if (
            not filesystem.directory_tab[d].sub_direcotories
            and not filesystem.directory_tab[d].file_names
        ):
            filesystem.directory_tab[d].size = -1

    # pprint(filesystem.directory_tab["wmsb"])

    calc_dir_sizes(filesystem)
    # pprint(filesystem.directory_tab)

    answer = 0
    for directory in list(filesystem.directory_tab.keys()):
        size = filesystem.directory_tab[directory].size
        if size <= 100000 and size > 0:
            answer += size
            print(filesystem.directory_tab[directory].dir_name)

    print(answer)


if __name__ == "__main__":
    main()
