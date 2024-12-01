# AOC22 D13p2: Distress Signal

import os

from functools import cmp_to_key


def compare_pair(left_element: int | list[int], right_element: int | list[int]) -> int:
    if isinstance(left_element, int) and isinstance(right_element, int):
        if left_element == right_element:
            return 0
        elif left_element < right_element:
            return -1
        else:
            return 1
    elif isinstance(left_element, list) and isinstance(right_element, list):
        for sub_left_element, sub_right_element in zip(left_element, right_element):
            match compare_pair(sub_left_element, sub_right_element):
                case 1:
                    return 1
                case 0:
                    continue
                case -1:
                    return -1
        else:
            if len(left_element) == len(right_element):
                return 0
            elif len(left_element) < len(right_element):
                return -1
            else:
                return 1
    elif isinstance(left_element, list) and isinstance(right_element, int):
        return compare_pair(left_element, [right_element])
    elif isinstance(left_element, int) and isinstance(right_element, list):
        return compare_pair([left_element], right_element)
    else:
        assert False, f"Unreacheable {type(left_element), type(right_element)}"


def parse_input_file(input_path: str) -> list[int | list]:
    packets: list[int | list] = list()
    with open(input_path) as f:
        raw_input: list[str] = f.read().split("\n\n")
    raw_input = [item for pair in raw_input for item in pair.split()]

    for packet in raw_input:
        packets.append(eval(packet))
    return packets


def main() -> None:
    input_path: str = os.path.dirname(__file__) + "\\input.txt"
    packets: list[int | list] = parse_input_file(input_path)

    packets.append([[2]])
    packets.append([[6]])

    packets = sorted(packets, key=cmp_to_key(compare_pair))

    print((packets.index([[2]]) + 1) * (packets.index([[6]]) + 1))


if __name__ == "__main__":
    main()
