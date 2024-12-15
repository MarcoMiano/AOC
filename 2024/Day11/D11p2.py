# AOC24 D11p2: Plutionian Pebbles
import os

from collections import defaultdict


def parse_input(input_path: str) -> defaultdict[int, int]:
    with open(input_path, "r") as f:
        raw_stones: list[str] = f.read().split()
    stones = defaultdict(int)
    for stone in raw_stones:
        stones[int(stone)] += 1
    return stones


def even_digits(x: int) -> bool:
    return len(str(x)) % 2 == 0


def blink(stones: defaultdict[int, int]) -> defaultdict[int, int]:
    new_stones = defaultdict(int)

    for key, value in stones.items():
        if key == 0:
            new_stones[1] += value
        elif even_digits(key):
            half = len(str(key)) // 2
            new_stones[int(str(key)[:half])] += value
            new_stones[int(str(key)[half:])] += value
        else:
            new_stones[key * 2024] += value
    return new_stones


def main() -> None:
    input_path: str = os.path.dirname(__file__) + "\\input.txt"
    stones: defaultdict[int, int] = parse_input(input_path)

    for j in range(75):
        print(j)
        stones = blink(stones)

    result = 0
    for stone in stones.values():
        result += stone
    print(result)


if __name__ == "__main__":
    main()
