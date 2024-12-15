# AOC24 D11p1: Plutionian Pebbles
import os


def parse_input(input_path: str) -> list[int]:
    with open(input_path, "r") as f:
        raw_stones: list[str] = f.read().split()
    return [int(stone) for stone in raw_stones]


def even_digits(x: int) -> bool:
    return len(str(x)) % 2 == 0


def main() -> None:
    input_path: str = os.path.dirname(__file__) + "\\input.txt"
    stones = parse_input(input_path)

    for _ in range(25):
        i = 0
        while i < len(stones):
            match stones[i]:
                case 0:
                    stones[i] = 1
                    i += 1
                case _ if even_digits(stones[i]):
                    s = str(stones[i])
                    half = len(s) // 2
                    stones.insert(i, int(s[:half]))
                    i += 1
                    stones[i] = int(s[half:])
                    i += 1
                case _:
                    stones[i] *= 2024
                    i += 1

    print(len(stones))


if __name__ == "__main__":
    main()
