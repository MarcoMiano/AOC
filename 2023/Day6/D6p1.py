# AOC23 D6p1: Wait For It
import re
import math


def parse_input_file(input_file: list[str]) -> list:
    output = list()

    input_file[0] = input_file[0].split(":")[1].strip()
    input_file[0] = re.sub(r"\s+", ";", input_file[0]).split(";")

    input_file[1] = input_file[1].split(":")[1].strip()
    input_file[1] = re.sub(r"\s+", ";", input_file[1]).split(";")

    if input_file[0].__len__() != input_file[1].__len__():
        raise ValueError("Different numbers of elements in times and distances list")

    for i in range(input_file[0].__len__()):
        output.append([int(input_file[0][i]), int(input_file[1][i])])

    return output


def main() -> None:
    with open("2023//Day6//input.txt") as f:
        input_file = f.read().strip().split("\n")

    races = parse_input_file(input_file)

    wins = 1

    for time, record_distance in races:
        charge_of_record1 = (time - math.sqrt(time**2 - 4 * record_distance)) / 2
        charge_of_record2 = (time + math.sqrt(time**2 - 4 * record_distance)) / 2
        charge_of_record = min(charge_of_record1, charge_of_record2)

        race_wins = (time - (int(charge_of_record) * 2)) - 1

        wins *= race_wins

    print(wins)


if __name__ == "__main__":
    main()
