# AOC23 D1p2: Trebuchet?!
import regex as re


def first_non_empty_element(lst: list) -> str:
    for element in lst:
        if element:
            return element


def written_number_to_int(string: str) -> int:
    match string.lower():
        case "one":
            return 1
        case "two":
            return 2
        case "three":
            return 3
        case "four":
            return 4
        case "five":
            return 5
        case "six":
            return 6
        case "seven":
            return 7
        case "eight":
            return 8
        case "nine":
            return 9
        case _:
            raise ValueError("Invalid string.")


answer = 0

with open("2023//Day1//input.txt", "r") as lines:
    for line in lines:
        line = line.strip("\n")
        matches = re.findall(
            r"(one|two|three|four|five|six|seven|eight|nine)|(\d)|(\d(?=\D*$))",
            line,
            overlapped=True,
        )

        first_match = first_non_empty_element(matches[0])

        try:
            first_digit = int(first_match)
        except ValueError:
            first_digit = written_number_to_int(first_match)

        last_match = first_non_empty_element(matches[-1])
        try:
            last_digit = int(last_match)
        except ValueError:
            last_digit = written_number_to_int(last_match)

        answer += (first_digit * 10) + last_digit


print(answer)
