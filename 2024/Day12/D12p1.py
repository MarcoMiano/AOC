# AOC24 D12p1: Garden Groups
import os
from collections import deque
from typing import Generator

DIRECTIONS: list[tuple[int, int]] = [(-1, 0), (0, 1), (1, 0), (0, -1)]


class Plots(object):
    def __init__(self) -> None:
        self._tiles: list[tuple[int, int]] = list()

    def __repr__(self) -> str:
        return repr(self._tiles)

    def _find_groups(self) -> Generator[set[tuple[int, int]]]:
        tiles_set = set(self._tiles)
        visited = set()

        def bfs(start: tuple[int, int]) -> set[tuple[int, int]]:
            queue = deque([start])
            group = set()
            while queue:
                tile = queue.popleft()
                if tile in visited:
                    continue
                visited.add(tile)
                group.add(tile)
                for direction in DIRECTIONS:
                    neighbor = tile[0] + direction[0], tile[1] + direction[1]
                    if neighbor in tiles_set and neighbor not in visited:
                        queue.append(neighbor)
            return group

        for tile in self._tiles:
            if tile not in visited:
                yield bfs(tile)

    def _exposed_sides(self, tile_pos: tuple[int, int]) -> int:
        result = 0
        for direction in DIRECTIONS:
            next_tile: tuple[int, int] = (
                tile_pos[0] + direction[0],
                tile_pos[1] + direction[1],
            )
            if next_tile not in self._tiles:
                result += 1
        return result

    def add_tile(self, tile_pos: tuple[int, int]):
        self._tiles.append(tile_pos)

    @property
    def area_perimeter(self) -> Generator[tuple[int, int]]:
        perimeter = 0
        for sub_plot in self._find_groups():
            for tile in sub_plot:
                perimeter += self._exposed_sides(tile)
            yield len(sub_plot), perimeter
            perimeter = 0


def parse_input(input_path: str) -> dict[str, Plots]:
    with open(input_path, "r") as f:
        raw_tiles: list[str] = f.read().strip().splitlines()
    garden: dict[str, Plots] = dict()
    for r, row in enumerate(raw_tiles):
        for c, char in enumerate(row):
            if char not in garden.keys():
                garden[char] = Plots()
            garden[char].add_tile((r, c))
    return garden


def even_digits(x: int) -> bool:
    return len(str(x)) % 2 == 0


def main() -> None:
    input_path: str = os.path.dirname(__file__) + "\\input.txt"
    garden: dict[str, Plots] = parse_input(input_path)

    cost = 0
    for key, plot in garden.items():
        for area, perimeter in plot.area_perimeter:
            cost += area * perimeter

    print(cost)


if __name__ == "__main__":
    main()
