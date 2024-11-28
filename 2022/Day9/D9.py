# AOC22 D9p1: Rope Bridge
# Copied from https://aoc.just2good.co.uk/2022/9
import os
from typing import TypeAlias, Iterator
from math import copysign
from dataclasses import dataclass

t_instruction: TypeAlias = tuple[str, int]
t_instructions: TypeAlias = list[t_instruction]

ROPE_LEN = 10


@dataclass(frozen=True)
class Point:
    """Class for storing a point x,y coordinate"""

    x: int
    y: int

    # create a list of (x,y) vectors that surround and include this point
    WITHIN_ONE = [(dx, dy) for dx in range(-1, 2) for dy in range(-1, 2)]

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)


VECTORS = {"U": Point(0, 1), "R": Point(1, 0), "D": Point(0, -1), "L": Point(-1, 0)}


class RopeSim:
    """Simulates a rope with a number of knots. We move the head according to a set of instructions.
    Here we model the movement of the knots behind the head, according to the rules specified.
    """

    def __init__(self, motions: list[tuple[str, int]], num_knots: int) -> None:
        """Expects a list of instructions in the format:
        [['R', 5], ['U', 8], ...]

        Models rope with num_knots. The first is the head, and the last is the tail."""
        self._instructions = motions
        self._num_knots = num_knots
        self._knots = [Point(0, 0) for _ in range(self._num_knots)]

    @staticmethod
    def _get_next_move(vector: Point) -> Point:
        x_move = 0
        y_move = 0
        move_x = False
        move_y = False

        if vector.y == 0:  # we only need to move left or right
            move_x = True
        elif vector.x == 0:  # we only need to move up or down
            move_y = True
        else:  # we need to move diagonally
            assert vector.x != 0 and vector.y != 0, "We must move diagonally"
            move_x = move_y = True

        if move_x:
            x_move = 1 if vector.x > 0 else -1

        if move_y:
            y_move = 1 if vector.y > 0 else -1

        return Point(x_move, y_move)

    def pull_rope(self) -> set[Point]:
        """Simulate the rope knot movemens, according to the rules given."""

        visited_locations: set[Point] = set()
        visited_locations.add(self._knots[-1])  # track the tail

        for direction, mag in self._instructions:  # read char by char
            for _ in range(mag):  # move one step at a time
                # print(f"Tail: {knots[-1]}; unique positions: {len(visited_locations)}")
                self._knots[0] += VECTORS[direction]  # move the head

                for i in range(1, len(self._knots)):  # move the tail
                    vector = self._knots[i - 1] - self._knots[i]

                    if vector in [Point(x, y) for (x, y) in Point.WITHIN_ONE]:
                        continue  # don't need to move
                    else:
                        self._knots[i] = self._knots[i] + RopeSim._get_next_move(vector)
                        visited_locations.add(self._knots[-1])

        return visited_locations


def main() -> None:
    input_path = os.path.dirname(__file__) + "\\input.txt"
    with open(input_path, mode="rt") as f:
        # convert to list of (direction, magnitude)
        data = [
            (d, int(v))
            for d, v in [instruction.split() for instruction in f.read().splitlines()]
        ]

    rope_sim = RopeSim(data, 10)
    visited_locations = rope_sim.pull_rope()
    print(len(visited_locations))


if __name__ == "__main__":
    main()
