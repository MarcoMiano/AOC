import argparse
import os
from datetime import datetime
from typing import Callable


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create skeleton folders and files for Advent of Code"
    )
    parser.add_argument(
        "--if_executed", "-if", action="store_true", help="Simulate execution"
    )
    parser.add_argument(
        "--year",
        "-y",
        type=str,
        default=str(datetime.now().year),
        help="Year of Advent of Code",
    )
    parser.add_argument(
        "--day",
        "-d",
        nargs=2,
        type=int,
        default=[1, 25],
        help="Range of day folders to create, eg. --day 1 24",
    )
    parser.add_argument(
        "--py_file",
        "-py",
        action="store_true",
        help="Create empty python files, eg. D5p1.py, D5p2.py",
    )
    parser.add_argument(
        "--files",
        "-f",
        nargs="*",
        type=str,
        default=[],
        help="File names to create, eg. -f input-sm.txt input.txt",
    )
    s_args = parser.parse_args()

    def execute(callback: Callable, *args, **kwargs):
        if not s_args.if_executed:
            return callback(*args, **kwargs)
        print(
            f"Simulate: {callback.__name__}({", ".join(map(str, args))}{", ".join(f'{k}={repr(v)}' for k, v in kwargs.items())})"
        )

    print(s_args)

    path = os.path.dirname(__file__) + "\\" + s_args.year

    if not os.path.isdir(path):
        execute(os.mkdir, path=path)

    for i in range(s_args.day[0], s_args.day[1] + 1):
        path_day = path + f"\\Day{i}"
        if not os.path.isdir(path_day):
            execute(os.mkdir, path=path_day)
        for file in s_args.files:
            path_file = path_day + f"\\{file}"
            if not os.path.isfile(path_file):
                execute(open, file=path_file, mode="a")
        if s_args.py_file:
            for j in range(1, 3):
                path_py_file = path_day + f"\\D{i}p{j}.py"
                execute(open, file=path_py_file, mode="a")


if __name__ == "__main__":
    main()
