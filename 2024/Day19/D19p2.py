# AOC24 D19p1: Linen Layout
import os
from functools import cache


def parse_input(input_path: str) -> tuple[list[str], list[str]]:
    blocks: list[str] = open(input_path).read().split("\n\n")
    return blocks[0].split(", "), blocks[1].splitlines()


def ways(design: str, pieces: set[str], lengths: list[int], alphabet: set[str]) -> int:
    if any(ch not in alphabet for ch in design):
        return 0

    @cache
    def dp(i: int) -> int:
        if i == len(design):
            return 1
        total = 0
        for L in lengths:
            if i + L <= len(design) and design[i : i + L] in pieces:
                total += dp(i + L)
        return total

    return dp(0)


def total_ways(pieces: list[str], designs: list[str]) -> int:
    pieceset: set[str] = set(pieces)
    lengths = sorted({len(p) for p in pieces}, reverse=True)
    alphabet = {ch for p in pieces for ch in p}

    total = 0
    for d in designs:
        w = ways(d, pieceset, lengths, alphabet)
        total += w
    return total


def main() -> None:
    input_path: str = os.path.dirname(__file__) + "\\input.txt"
    pieces, designs = parse_input(input_path)
    print(total_ways(pieces, designs))


if __name__ == "__main__":
    main()
