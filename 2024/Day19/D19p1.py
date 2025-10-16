# AOC24 D19p1: Linen Layout
import os
from functools import cache


def parse_input(input_path: str) -> tuple[list[str], list[str]]:
    blocks: list[str] = open(input_path).read().split("\n\n")
    return blocks[0].split(", "), blocks[1].splitlines()


def can_make(design: str, pieces: set[str], lengths: set[int]) -> bool:
    @cache
    def can(i: int) -> bool:
        if i == len(design):
            return True
        for L in lengths:
            if i + L <= len(design) and design[i : i + L] in pieces:
                if can(i + L):
                    return True
        return False

    return can(0)


def count_buildable(pieces: list[str], designs: list[str]) -> int:
    pieceset: set[str] = set(pieces)
    lengths = {len(p) for p in pieces}
    count = 0
    for design in designs:
        if can_make(design, pieceset, lengths):
            count += 1
    return count


def main() -> None:
    input_path: str = os.path.dirname(__file__) + "\\input-sm.txt"
    pieces, designs = parse_input(input_path)
    print(count_buildable(pieces, designs))


if __name__ == "__main__":
    main()
