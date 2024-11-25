# AOC22 D9p1: Rope Bridge
import os
from typing import TypeAlias, Iterator
from math import copysign

t_instruction: TypeAlias = tuple[str, int]
t_instructions: TypeAlias = list[t_instruction]


ROPE_LEN = 2


class Vec2(object):
    def __init__(self, x, y) -> None:
        self.x, self.y = x, y

    def __add__(self, other: "Vec2") -> "Vec2":
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vec2") -> "Vec2":
        return Vec2(self.x - other.x, self.y - other.y)

    def __iadd__(self, other: "Vec2") -> "Vec2":
        self = self + other
        return self

    def __iter__(self) -> Iterator:
        return iter(self.x, self.y)


def Vec2_avt(vec: "Vec2") -> "Vec2":
    # Absolute Value Transformation
    return Vec2(abs(vec.x), abs(vec.y))


def Vec2_eq(vec1: "Vec2", vec2: "Vec2") -> bool:
    return (vec1.x == vec2.x) and (vec1.y == vec2.y)


t_position: TypeAlias = dict[str, Vec2]


DIRECTIONS: dict[str, Vec2] = {
    "R": Vec2(1, 0),
    "D": Vec2(0, -1),
    "L": Vec2(-1, 0),
    "U": Vec2(0, 1),
    "N": Vec2(0, 0),
}


class Knot(object):
    def __init__(self, init_pos: Vec2) -> None:
        self.position: Vec2 = init_pos
        self.last_dir: str = "S"

    def __sub__(self, other: "Knot") -> Vec2:
        return self.position - other.position

    # def __iadd__(self, other: Vec2) -> None:
    #     self.position += other

    def move(self, direction: str) -> None:
        self.position += DIRECTIONS[direction]
        self.last_dir = direction

    def is_touching(self, other: "Knot") -> bool:
        if 0 <= max(self - other) <= 1:
            return True
        else:
            return False

    def is_diagonal(self, other: "Knot") -> bool:
        # #######
        # ##D#D##
        # #D###D#
        # ###1###
        # #D###D#
        # ##D#D##
        # #######
        diff: Vec2 = Vec2_avt(self - other)
        if Vec2_eq(diff, Vec2(1, 2)) or Vec2_eq(diff, Vec2(2, 1)):
            return True
        else:
            return False


def calc_next_dir(knot1: Knot, knot2: Knot) -> list[str]:
    if knot2.is_touching(knot1):
        # Knots are touching so knot2 doesn't need to move
        return ["N"]
    elif not knot2.is_touching(knot1) and knot2.is_diagonal(knot1):
        # Knots are not touching and knot2 has to move in a diagonal move
        diff: Vec2 = knot1 - knot2
        if Vec2_eq(diff, Vec2(1,2)) or Vec2_eq(diff, Vec2(2, 1)):
            return ["U", "R"]
        elif Vec2_eq(diff,)



class Rope(object):
    def __init__(self, rope_len: int) -> None:
        self.knot_list: list[Knot] = list()
        for _ in range(rope_len):
            self.add_knot(Knot(Vec2(0, 0)))

    def add_knot(self, knot: Knot) -> None:
        # First knot in list is considered the HEAD, the last is the TAIL
        self.knot_list.append(knot)

    def simulate_inst(self, instruction: t_instruction) -> None:
        assert (
            self.knot_list is None
        ), "ERROR: Rope.simulate_inst - self.knot_list is None"
        direction, steps = instruction
        for i in range(1, steps + 1):
            # Move the head knot
            self.knot_list[0].move(direction)

            # Move the other knots
            for i in range(len(self.knot_list)):
                direction: str = calc_next_dir(self.knot_list[i], self.knot_list[i + 1])


def parse_input_file(path) -> t_instructions:
    with open(path) as f:
        instructions: t_instructions = []
        for row in f.readlines():
            raw_ins: list[str] = row.strip().split()
            instructions.append((raw_ins[0], int(raw_ins[1])))
    return instructions


def main() -> None:
    input_path = os.path.dirname(__file__) + "\\input.txt"
    instructions: t_instructions = parse_input_file(input_path)
    rope = Rope(ROPE_LEN)

    for instruction in instructions:
        rope.simulate_inst(instruction)


if __name__ == "__main__":
    main()
