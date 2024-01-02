# AOC23 D15p2: Lens Library
from collections import defaultdict, OrderedDict
import re
from typing import DefaultDict, OrderedDict

# LPF-HASH -> Lava Production Facility-Holiday ASCII Helper Algorithm


def get_lpf_hash(string: str) -> int:
    output = 0
    for char in string:
        output += ord(char)
        output *= 17
        output %= 256
    return output


def get_checksum(strings: list[str]) -> int:
    output = 0

    for string in strings:
        output += get_lpf_hash(string)

    return output


def execute_steps(init_seq) -> DefaultDict[int, OrderedDict[str, int]]:
    def split_step(step: str) -> tuple[str, int, bool, int]:
        label = re.sub(r"[^a-zA-Z]", "", step)
        box_number: int = get_lpf_hash(label)
        remove: bool = True if "-" in step else False
        focal_length: int = int(re.sub(r"[^0-9]", "", step)) if not remove else 0

        return label, box_number, remove, focal_length

    boxes = defaultdict()
    for step in init_seq:
        label, box_number, remove, focal_leght = split_step(step)

        if remove:
            try:
                boxes[box_number].pop(label)
            except:
                pass

        else:
            try:
                boxes[box_number][label] = focal_leght
            except KeyError:
                boxes[box_number] = OrderedDict()
                boxes[box_number][label] = focal_leght
    return boxes


def main() -> None:
    with open("Day15\\input.txt") as f:
        init_seq: list[str] = f.read().strip("\n").split(",")

    focusing_power = 0

    boxes = execute_steps(init_seq)

    for b, box in boxes.items():
        for f, (_, focal_leght) in enumerate(box.items()):
            focusing_power += (b + 1) * (f + 1) * focal_leght

    print(focusing_power)


if __name__ == "__main__":
    main()
