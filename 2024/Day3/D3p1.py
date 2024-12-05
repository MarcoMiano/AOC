# AOC24 D3p1: Mull It Over

import os
import re

from typing import Any


def parse_input(input_path) -> list[tuple[int, int]]:
    with open(input_path) as f:
        raw_memory = f.read()
    muls = re.findall(r"mul\((\d+),(\d+)\)", raw_memory, flags=re.MULTILINE)
    return muls


def main() -> None:
    input_path: str = os.path.dirname(__file__) + "\\input.txt"
    muls: list[tuple[int, int]] = parse_input(input_path)
    result = 0
    for pair in muls:
        result += int(pair[0]) * int(pair[1])

    print(result)


if __name__ == "__main__":
    main()
