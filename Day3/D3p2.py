# AOC23 D3p1: Gear Ratios
import re


def check_if_gear(input_file: list[str], line_id: int, pos: int) -> int:
    """Check if the * in input_file[line_id][pos] is a gear and return the gear ratio

    Args:
        input_file (list[str]): list of strings that contains gears and part numbers
        line_id (int): index pointing to which line the possible gear is found
        pos (int): index pointing to which caracter of line the possible gear is found

    Returns:
        int: gear ratio
    """
    count = 0
    output = 1
    for x in range(max(0, line_id - 1), min(line_id + 2, len(input_file))):
        input_file_slicer = slice(max(0, pos - 4), min(pos + 3, len(input_file[x])))
        for match in re.finditer(r"\d+", input_file[x][input_file_slicer]):
            match_start_is_near = (match.start() + 1) in range(3, 6)
            match_end_is_near = match.end() in range(3, 6)
            if match_start_is_near or match_end_is_near:
                count += 1
                output *= int(match.group())
    return output if count > 1 else 0


def main() -> None:
    with open("input.txt") as file:
        input_file = file.read().strip().split("\n")

    answer = 0

    for line_id, line in enumerate(input_file):
        for match in re.finditer(r"\*", line):
            answer += check_if_gear(input_file, line_id, match.end())

    print(answer)


if __name__ == "__main__":
    main()
