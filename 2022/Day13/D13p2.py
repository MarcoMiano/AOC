# AOC22 D13p1: Distress Signal
import os

from typing import TypeAlias
from pprint import pprint

t_packets: TypeAlias = list[tuple[list[int], list[int]]]


def parse_input_file(input_path: str) -> t_packets:
    packets: t_packets = list()
    with open(input_path) as f:
        raw_input: list[str] = f.read().split("\n\n")

    for pair in raw_input:
        left, right = pair.split()
        packets.append((eval(left.strip()), eval(right.strip())))
    return packets


def compare_pair(left_element: int | list[int], right_element: int | list[int]) -> int:
    if isinstance(left_element, int) and isinstance(right_element, int):
        if left_element == right_element:
            return 0
        elif left_element < right_element:
            return 1
        else:
            return -1
    elif isinstance(left_element, list) and isinstance(right_element, list):
        for sub_left_element, sub_right_element in zip(left_element, right_element):
            match compare_pair(sub_left_element, sub_right_element):
                case -1:
                    return -1
                case 0:
                    continue
                case 1:
                    return 1
        else:
            if len(left_element) == len(right_element):
                return 0
            elif len(left_element) < len(right_element):
                return 1
            else:
                return -1
    elif isinstance(left_element, list) and isinstance(right_element, int):
        return compare_pair(left_element, [right_element])
    elif isinstance(left_element, int) and isinstance(right_element, list):
        return compare_pair([left_element], right_element)
    else:
        assert False, f"Unreacheable {type(left_element), type(right_element)}"


def main() -> None:
    input_path: str = os.path.dirname(__file__) + "\\input.txt"
    packets: t_packets = parse_input_file(input_path)

    ok_pairs = 0
    for i, (left, right) in enumerate(packets):
        result = compare_pair(left, right)
        if result > 0:
            ok_pairs += i + 1
            continue
        else:
            continue

    print(ok_pairs)


if __name__ == "__main__":
    main()
