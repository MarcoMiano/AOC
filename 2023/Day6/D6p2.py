# AOC23 D6p2: Wait For It
import re
import math


def parse_input_file(input_file: list[str]) -> list:
    input_file[0] = input_file[0].split(":")[1].strip()
    input_file[0] = int(re.sub(r"\s+", "", input_file[0]))

    input_file[1] = input_file[1].split(":")[1].strip()
    input_file[1] = int(re.sub(r"\s+", "", input_file[1]))

    print(input_file)

    return input_file


def main() -> None:
    with open("2023//Day6//input.txt") as f:
        input_file = f.read().strip().split("\n")

    time, record_distance = parse_input_file(input_file)

    charge_of_record1 = (time - math.sqrt(time**2 - 4 * record_distance)) / 2
    charge_of_record2 = (time + math.sqrt(time**2 - 4 * record_distance)) / 2
    charge_of_record = min(charge_of_record1, charge_of_record2)

    answer = (time - (int(charge_of_record) * 2)) - 1

    print(answer)


if __name__ == "__main__":
    main()
