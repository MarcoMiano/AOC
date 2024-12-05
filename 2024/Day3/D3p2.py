# AOC24 D3p2: Mull It Over
import os
import re


def parse_input(input_path) -> list:
    muls: list = list()
    with open(input_path) as f:
        raw_memory = f.read()
    raw_muls = re.split(r"(do\(\)|don\'t\(\))", raw_memory)

    do = True
    for section in raw_muls:
        if section == "do()":
            do = True
            continue
        if section == "don't()":
            do = False
            continue
        if do:
            muls.extend(re.findall(r"mul\((\d+),(\d+)\)", section, flags=re.MULTILINE))
            continue

    return muls


def main() -> None:
    input_path: str = os.path.dirname(__file__) + "\\input.txt"
    muls: list[tuple[int, int]] = parse_input(input_path)
    result = 0
    for pair in muls:
        result += int(pair[0]) * int(pair[1])

    print(result)


if __name__ == "__main__":
    main()
