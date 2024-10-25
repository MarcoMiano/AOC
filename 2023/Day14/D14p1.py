# AOC23 D14p1: Parabolic Reflector Dish

from collections import deque


def find_all_blocks(column: str, block_pos: deque[int]) -> None:
    for c, char in enumerate(column):
        if char == "#":
            block_pos.append(c)
        if c == len(column) - 1:
            block_pos.append(c + 1)


def get_column_load(segments: list[str], block_pos: deque[int]) -> int:
    column_load = 0
    for segment in segments:
        wheight = block_pos.popleft()

        if not segment:
            continue

        round_stone_count = segment.count("O")
        for i in range(round_stone_count):
            column_load += wheight - i

    return column_load


def main() -> None:
    with open("Day14\\input.txt") as f:
        platform = f.read().strip().splitlines()

    platform = list(zip(*platform[::-1]))
    platform = ["".join(line) for line in platform]

    total_load = 0
    for column in platform:
        block_pos = deque()
        find_all_blocks(column, block_pos)
        column = column.split("#")
        total_load += get_column_load(column, block_pos)
    print(total_load)


if __name__ == "__main__":
    main()
