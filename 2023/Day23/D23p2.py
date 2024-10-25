# AOC23 D23p2: A Long Walk
from typing import TypeAlias
from copy import deepcopy
from functools import cache
import time

t_map: TypeAlias = list[list[str]]
t_direction: TypeAlias = tuple[int, int]
t_coord: TypeAlias = tuple[int, int]

DOWN: t_direction = (1, 0)
UP: t_direction = (-1, 0)
LEFT: t_direction = (0, -1)
RIGHT: t_direction = (0, 1)

DIRECTIONS: list[t_direction] = [UP, RIGHT, DOWN, LEFT]
INV_DIRECTIONS: dict[t_direction, t_direction] = {
    UP: DOWN,
    RIGHT: LEFT,
    DOWN: UP,
    LEFT: RIGHT,
}
DIRECTIONS_NAMES: dict[t_direction, str] = {
    UP: "UP",
    RIGHT: "RIGHT",
    DOWN: "DOWN",
    LEFT: "LEFT",
}

VALID_TILES: list[str] = [".", "<", "v", "^", ">"]


def load_map(file_name: str) -> t_map:
    final_map: t_map = list(list())
    with open(file_name) as f:
        lines: list[str] = f.read().strip().splitlines()
        for line in lines:
            final_map.append(list(line))
    return final_map


def print_map(aoc_map: list[list[str]]):
    for line in aoc_map:
        print(line)


def vect_add(list1: t_coord, list2: t_coord) -> t_coord:
    return (list1[0] + list2[0], list1[1] + list2[1])


def stroll(
    start_coord: t_coord,
    visited_coords: set[t_coord],
    direction: t_direction = DOWN,
    start_steps: int = 0,
) -> int:
    global aoc_map
    coord: t_coord = start_coord
    results = {0}
    steps = start_steps

    def find_next_direction() -> list[t_direction]:
        directions = list()

        if coord[0] == len(aoc_map) - 1:
            return [DOWN]

        for dir in DIRECTIONS:
            if dir == INV_DIRECTIONS[direction]:
                continue

            next_tile = aoc_map[coord[0] + dir[0]][coord[1] + dir[1]]
            if next_tile in VALID_TILES:
                directions.append(dir)

        return directions

    while coord[0] != len(aoc_map) - 1:
        steps += 1
        coord = vect_add(coord, direction)

        if coord in visited_coords:
            return max(results)
        else:
            visited_coords.add(coord)

        next_directions: list[t_direction] = find_next_direction()

        while len(next_directions) > 1:
            results.add(
                stroll(
                    coord,
                    deepcopy(visited_coords),
                    next_directions[-1],
                    steps,
                )
            )
            next_directions.pop()

        direction = next_directions[0]

    results.add(steps)
    return max(results)


start = time.time()
aoc_map: t_map = load_map("2023//Day23//input.txt")
start_coord: t_coord = (0, 1)
visited_coords: set[t_coord] = {start_coord}
result: int = stroll(start_coord, visited_coords)
print(result)
print(time.time() - start)
