# AOC23 D23p1: A Long Walk
from typing import TypeAlias
import asyncio

t_map: TypeAlias = list[list[str]]
t_direction: TypeAlias = tuple[int, int]


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
        for l, line in enumerate(lines):
            final_map.append(list(line))
    return final_map


def print_map(aoc_map: list[list[str]]):
    for line in aoc_map:
        print(line)


def vect_add(
    list1: list[int] | tuple[int, int], list2: list[int] | tuple[int, int]
) -> list[int]:
    return [list1[0] + list2[0], list1[1] + list2[1]]


async def stroll(
    aoc_map: t_map,
    start_coord: tuple[int, int] | list[int],
    direction: t_direction = DOWN,
    start_steps: int = 0,
) -> list[int]:
    coord: list[int] = list(start_coord)
    results = list()
    steps = start_steps

    def find_next_direction() -> list[t_direction]:
        directions = list()

        if coord[0] == len(aoc_map) - 1:
            return [DOWN]

        for dir in DIRECTIONS:
            next_tile = aoc_map[coord[0] + dir[0]][coord[1] + dir[1]]
            if dir == INV_DIRECTIONS[direction]:
                continue
            if next_tile in VALID_TILES:
                if (
                    (next_tile == "^" and dir == DOWN)
                    or (next_tile == ">" and dir == LEFT)
                    or (next_tile == "v" and dir == UP)
                    or (next_tile == "<" and dir == RIGHT)
                ):
                    continue
                directions.append(dir)
        assert len(directions) > 0

        return directions

    while coord[0] != len(aoc_map) - 1:
        steps += 1
        coord = vect_add(coord, direction)
        next_directions: list[t_direction] = find_next_direction()
        while len(next_directions) > 1:
            results += await stroll(aoc_map, coord, next_directions[-1], steps)
            next_directions.pop()

        direction = next_directions[0]

    results.append(steps)
    return results


async def main() -> None:
    forest_map: t_map = load_map("Day23\\input.txt")
    print(len(forest_map))
    start_coord: tuple[int, int] = (0, 1)
    results: list[int] = await stroll(forest_map, start_coord)
    print(max(results))


if __name__ == "__main__":
    asyncio.run(main())
