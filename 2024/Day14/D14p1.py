# AOC24 D14p1: Restroom Redoubt
import os
from typing import TypeAlias
import math

T_robots: TypeAlias = list[dict[str, tuple[int, ...]]]

MAP: tuple[int, int] = (11, 7)
# MAP: tuple[int, int] = (101, 103)
CYCLES: int = 100


def parse_input(input_path: str) -> T_robots:
    robots: T_robots = list()
    with open(input_path) as file:
        raw_robots = file.read().split("\n")

    for raw_robot in raw_robots:
        raw_p, raw_v = raw_robot.split(" ")
        p: tuple[int, ...] = tuple(map(int, raw_p.split("=")[1].split(",")))
        v: tuple[int, ...] = tuple(map(int, raw_v.split("=")[1].split(",")))
        robots.append({"p": p, "v": v})
    return robots


def find_quadrant(x, y) -> int | None:
    # 0|2
    # 1|3
    mid_x = MAP[0] // 2
    mid_y = MAP[1] // 2
    if x == mid_x or y == mid_y:
        return None

    top: bool = x < mid_x
    left: bool = y < mid_y

    match (top, left):
        case (True, True):
            return 0
        case (True, False):
            return 1
        case (False, True):
            return 2
        case (False, False):
            return 3


def simulate(cycles: int, robots: T_robots) -> int:
    # final_pos_x = start_pos_x + (vel_x * cycles) % MAP[0]
    # final_pos_y = start_pos_y + (vel_y * cycles) % MAP[1]
    quadrants: list[int] = [0, 0, 0, 0]
    for robot in robots:
        fpx: int = (robot["p"][0] + robot["v"][0] * cycles) % MAP[0]
        fpy: int = (robot["p"][1] + robot["v"][1] * cycles) % MAP[1]
        q = find_quadrant(fpx, fpy)
        if q is not None:
            quadrants[q] += 1
    return math.prod(quadrants)


def main() -> None:
    input_path: str = os.path.dirname(__file__) + "\\input.txt"
    robots = parse_input(input_path)
    # pprint(robots)
    print(simulate(CYCLES, robots))
    pass


if __name__ == "__main__":
    main()
