# AOC24 D1p1: Historian Hysteria
import os


def parse_input(input_path) -> tuple[list[int], list[int]]:
    l1: list[int] = list()
    l2: list[int] = list()

    with open(input_path) as f:
        raw_input: list[str] = f.readlines()

    for line in raw_input:
        id1, id2 = line.split()
        l1.append(int(id1))
        l2.append(int(id2))

    return l1, l2


def main() -> None:
    input_path: str = os.path.dirname(__file__) + "\\input.txt"
    l1, l2 = parse_input(input_path)
    l1.sort()
    l2.sort()
    distance = 0
    for id1, id2 in zip(l1, l2):
        distance += abs(id1 - id2)
    print(distance)


if __name__ == "__main__":
    main()
