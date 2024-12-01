# AOC24 D1p1: Historian Hysteria
import os
from collections import Counter


def parse_input(input_path) -> tuple[list[int], Counter[int]]:
    l1: list[int] = list()
    l2: list[int] = list()

    with open(input_path) as f:
        raw_input: list[str] = f.readlines()

    for line in raw_input:
        id1, id2 = line.split()
        l1.append(int(id1))
        l2.append(int(id2))

    return l1, Counter(l2)


def main() -> None:
    input_path: str = os.path.dirname(__file__) + "\\input.txt"
    l1, l2 = parse_input(input_path)
    similarity = 0
    for id1 in l1:
        similarity += id1 * l2[id1]
    print(similarity)


if __name__ == "__main__":
    main()
