# AOC23 D3p1: Gear Ratios
import re


def check_neighbors(input_file: list[str], line_id: int, start: int, end: int) -> bool:
    for x in range(max(0, line_id - 1), min(line_id + 2, len(input_file))):
        for y in range(max(0, start - 1), min(end + 1, len(input_file[x]))):
            if not (input_file[x][y].isdigit() or input_file[x][y] == "."):
                return True
    return False


def main() -> None:
    with open("input.txt") as file:
        input_file = file.read().strip().split("\n")

    answer = 0

    for line_id, line in enumerate(input_file):
        for match in re.finditer(r"\d+", line):
            num = match.group()
            answer += (
                int(num)
                if check_neighbors(input_file, line_id, match.start(), match.end())
                else 0
            )

    print(answer)


if __name__ == "__main__":
    main()
