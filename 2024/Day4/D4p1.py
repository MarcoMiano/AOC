# AOC24 D4p1: Ceres Search

import os

from typing import Any

DIRECTIONS: list[tuple[int, int]] = [
    (-1, 0),
    (-1, 1),
    (0, 1),
    (1, 1),
    (1, 0),
    (1, -1),
    (0, -1),
    (-1, -1),
]


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


def get_submatrix(matrix: list[list[str]], row: int, col: int) -> list[list[str]]:
    result = [list(), list(), list(), list(), list(), list(), list(), list()]
    rows: int = len(matrix)
    cols: int = len(matrix[0])
    for i, (dr, dc) in enumerate(DIRECTIONS):
        r, c = row, col
        result[i].append(matrix[r][c])
        for _ in range(3):
            r += dr
            c += dc
            if 0 <= r < rows and 0 <= c < cols:
                result[i].append(matrix[r][c])
            else:
                break
    return [element for element in result if len(element) == 4]


def check_xmas(matrix: list[list[str]], char: str = "X") -> int:
    result = 0
    x_indices: list[tuple[int, int]] = get_indices(matrix, char)
    for xr, xc in x_indices:
        for direction in get_submatrix(matrix, xr, xc):
            print("".join(direction))
            if "".join(direction) == "XMAS":
                result += 1

    return result


def main() -> None:
    input_path: str = os.path.dirname(__file__) + "\\input.txt"
    puzzle: list[list[str]] = parse_input(input_path)

    word_count = check_xmas(puzzle)

    print(word_count)


if __name__ == "__main__":
    main()
