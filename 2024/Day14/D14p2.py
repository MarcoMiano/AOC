# AOC24 D14p2: Restroom Redoubt
import os
from typing import TypeAlias

T_robots: TypeAlias = list[dict[str, tuple[int, ...]]]

# MAP: tuple[int, int] = (11, 7)
MAP: tuple[int, int] = (101, 103)
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


def find_cluster(m: list[list[int]]) -> bool:
    for x in range(MAP[0] - 2):
        for y in range(MAP[1] - 2):
            block = [row[y : y + 3] for row in m[x : x + 3]]
            if all(all(x == 1 for x in row) for row in block):
                return True
    return False


def simulate(robots: T_robots) -> int:
    i = 0
    while True:
        robot_map: list[list[int]] = [[0] * MAP[1] for _ in range(MAP[0])]
        for robot in robots:
            fpx: int = (robot["p"][0] + robot["v"][0] * i) % MAP[0]
            fpy: int = (robot["p"][1] + robot["v"][1] * i) % MAP[1]
            robot_map[fpx][fpy] = 1
        if find_cluster(robot_map):
            # print(robot_map)
            return i
        i += 1


def main() -> None:
    input_path: str = os.path.dirname(__file__) + "\\input.txt"
    robots = parse_input(input_path)
    # pprint(robots)
    print(simulate(robots))
    pass


if __name__ == "__main__":
    main()
