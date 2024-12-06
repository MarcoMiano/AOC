# AOC24 D4p2: Ceres Search

import os

from typing import Any


def parse_input(input_path) -> list[list[str]]:
    with open(input_path) as f:
        puzzle: list[list[str]] = [
            [char for char in line.strip()] for line in f.readlines()
        ]
    return puzzle


def get_indices(matrix: list[list[str]], search: str) -> list[tuple[int, int]]:
    return [
        (r, c)
        for r, row in enumerate(matrix)
        for c, char in enumerate(row)
        if char == search
    ]


def check_xmas(matrix: list[list[str]]) -> int:
    result = 0
    a_indices: list[tuple[int, int]] = get_indices(matrix, "A")
    for ar, ac in a_indices:
        if not (0 < ar < len(matrix) - 1 and 0 < ac < len(matrix[ac]) - 1):
            continue
        d1: str = "".join(
            [matrix[ar - 1][ac - 1], matrix[ar][ac], matrix[ar + 1][ac + 1]]
        )
        d2: str = "".join(
            [matrix[ar + 1][ac - 1], matrix[ar][ac], matrix[ar - 1][ac + 1]]
        )
        if (d1 == "MAS" or d1 == "SAM") and (d2 == "MAS" or d2 == "SAM"):
            result += 1

    return result


def main() -> None:
    input_path: str = os.path.dirname(__file__) + "\\input.txt"
    puzzle: list[list[str]] = parse_input(input_path)

    word_count = check_xmas(puzzle)

    print(word_count)


if __name__ == "__main__":
    main()
