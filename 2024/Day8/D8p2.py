# AOC24 D8p2: Resonant Collinearity
import os

from collections import defaultdict
from itertools import combinations


def parse_input(input_path: str) -> tuple[defaultdict[str, list[tuple[int, int]]], int]:
    with open(input_path, "r") as f:
        lines: list[str] = f.read().strip().splitlines()

    result: defaultdict[str, list[tuple[int, int]]] = defaultdict(list)
    for l, line in enumerate(lines):
        for c, char in enumerate(line):
            if char != ".":
                result[char].append((l, c))
    return result, len(lines)


def get_antinode(
    a: tuple[int, int], b: tuple[int, int], limit: int
) -> set[tuple[int, int]]:
    def in_bounds(c1: int, c2: int) -> bool:
        return 0 <= c1 < limit and 0 <= c2 < limit

    result = set()

    ax, ay = a
    result.add(a)
    bx, by = b
    result.add(b)

    i = 1
    cx, cy = ax - i * (bx - ax), ay - i * (by - ay)
    while in_bounds(cx, cy):
        result.add((cx, cy))
        i += 1
        cx, cy = ax - i * (bx - ax), ay - i * (by - ay)

    i = 1
    dx, dy = bx + i * (bx - ax), by + i * (by - ay)
    while in_bounds(dx, dy):
        result.add((dx, dy))
        i += 1
        dx, dy = bx + i * (bx - ax), by + i * (by - ay)

    return result


def main() -> None:
    input_path: str = os.path.dirname(__file__) + "\\input.txt"
    frequencies, limit = parse_input(input_path)

    result = set()
    for locs in frequencies.values():
        for a, b in combinations(locs, r=2):
            result.update(get_antinode(a, b, limit))

    print(len(result))


if __name__ == "__main__":
    main()
