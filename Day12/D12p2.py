# AOC23 D12p1: Hot Springs
from functools import cache


@cache
def find_arrangements(config: str, numbers: tuple) -> int:
    if config == "":
        return 1 if numbers == () else 0

    if numbers == ():
        return 0 if "#" in config else 1

    result = 0

    if config[0] in ".?":
        result += find_arrangements(config[1:], numbers)

    if config[0] in "#?":
        if (
            numbers[0] <= len(config)
            and "." not in config[: numbers[0]]
            and (numbers[0] == len(config) or config[numbers[0]] != "#")
        ):
            result += find_arrangements(config[numbers[0] + 1 :], numbers[1:])

    return result


def main() -> None:
    with open("Day12\\input.txt") as f:
        input_file = f.read().strip().splitlines()

    answer = 0

    for line in input_file:
        config, numbers = line.split()
        config = "?".join([config] * 5)

        numbers = tuple(map(int, numbers.split(",")))
        numbers *= 5

        answer += find_arrangements(config, numbers)

    print(answer)


if __name__ == "__main__":
    main()
