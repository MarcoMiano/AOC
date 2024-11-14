# AOC22 D9p1: Rope Bridge
import os
from typing import TypeAlias
from math import copysign

t_instructions: TypeAlias = list[tuple[str, int]]
t_position: TypeAlias = dict[str, tuple[int, int]]

DIRECTIONS: dict[str, tuple[int, int]] = {
    "R": (1, 0),
    "D": (0, -1),
    "L": (-1, 0),
    "U": (0, 1),
}


def parse_input_file(path) -> t_instructions:
    with open(path) as f:
        instructions: t_instructions = []
        for row in f.readlines():
            raw_ins = row.strip().split()
            instructions.append((raw_ins[0], int(raw_ins[1])))
    return instructions


def sum_tuple(t1: tuple[int, int], t2: tuple[int, int]) -> tuple[int, int]:
    return (t1[0] + t2[0], t1[1] + t2[1])


def check_tail(t1: tuple[int, int], t2: tuple[int, int]) -> tuple[bool, bool]:
    touch: bool = 0 <= abs(t1[0] - t2[0]) < 2 and 0 <= abs(t1[1] - t2[1]) < 2
    diagonal: bool = not touch and (abs(t1[0] - t2[0]) == 1 or abs(t1[1] - t2[1]) == 1)
    return touch, diagonal


def main() -> None:
    input_path: str = os.path.dirname(__file__) + "\\input.txt"
    instructions: t_instructions = parse_input_file(input_path)
    seen: set[tuple[int, int]] = set()
    last_position: t_position = {"H": (0, 0), "T": (0, 0)}
    seen.add(last_position["T"])
    # print(last_position)
    for dir, steps in instructions:
        assert dir in "RDLU"
        # print(dir, steps)
        while steps > 0:
            last_position["H"] = sum_tuple(last_position["H"], DIRECTIONS[dir])
            touch, diagonal = check_tail(last_position["H"], last_position["T"])
            if diagonal:
                if dir in "RL":
                    last_position["T"] = sum_tuple(last_position["T"], DIRECTIONS[dir])
                    last_position["T"] = (
                        last_position["T"][0],
                        last_position["T"][1]
                        + int(
                            copysign(1, last_position["H"][1] - last_position["T"][1])
                        ),
                    )
                    seen.add(last_position["T"])
                elif dir in "UD":
                    last_position["T"] = sum_tuple(last_position["T"], DIRECTIONS[dir])
                    last_position["T"] = (
                        last_position["T"][0]
                        + int(
                            copysign(1, last_position["H"][0] - last_position["T"][0])
                        ),
                        last_position["T"][1],
                    )
                    seen.add(last_position["T"])
                else:
                    assert False
            elif not touch:
                last_position["T"] = sum_tuple(last_position["T"], DIRECTIONS[dir])
                seen.add(last_position["T"])
            steps -= 1
            # print(last_position, touch, diagonal)
    print(len(seen))


if __name__ == "__main__":
    main()
