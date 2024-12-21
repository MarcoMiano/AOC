# AOC24 D12p2: Garden Groups
# https://github.com/RichRat/pyxercise/tree/master

import os


def greatest_common_divisor(a, b):
    if a == 0:
        return b
    if b == 0:
        return a
    if a < b:
        return greatest_common_divisor(b, a)
    return greatest_common_divisor(b, a % b)


class IntVector2:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __add__(self, other):
        return IntVector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return IntVector2(self.x - other.x, self.y - other.y)

    def __mul__(self, factor):
        if isinstance(factor, int):
            return IntVector2(self.x * factor, self.y * factor)
        else:
            raise Exception(
                "cannot multiply "
                + str(factor)
                + " with IntVector2 only int supported!"
            )

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def of_grid(self, grid):
        return grid[self.y][self.x]

    def set_grid(self, grid, val):
        grid[self.y][self.x] = val

    def is_in_bounds(self, grid):
        return 0 <= self.y < len(grid) and 0 <= self.x < len(grid[0])

    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

    def __hash__(self):
        return hash(str(self))

    def normalize(self):
        gcd = greatest_common_divisor(abs(self.x), abs(self.y))
        return IntVector2(int(self.x / gcd), int(self.y / gcd))


def grid_walk(grid: list[list]):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            yield IntVector2(x, y)


def grid_walk_val(grid: list[list]):
    for pos in grid_walk(grid):
        yield pos, pos.of_grid(grid)


def main() -> None:
    input_path: str = os.path.dirname(__file__) + "\\input.txt"
    with open(input_path) as list_file:
        grid = [[c for c in line] for line in list_file.read().split("\n")]

    added_grid = [[False] * len(row) for row in grid]
    dir_list = [IntVector2(*c) for c in [(1, 0), (0, 1), (-1, 0), (0, -1)]]

    # recursively find the area
    def find_area(letter, pos: IntVector2, group):
        for next_pos in [pos + dir for dir in dir_list]:
            if (
                next_pos.is_in_bounds(grid)
                and not next_pos.of_grid(added_grid)
                and next_pos.of_grid(grid) == letter
            ):
                group.append(next_pos)
                next_pos.set_grid(added_grid, True)
                find_area(letter, next_pos, group)

    result = 0
    for pos, val in grid_walk_val(grid):
        if pos.of_grid(added_grid):
            continue

        group = [pos]
        pos.set_grid(added_grid, True)
        find_area(val, pos, group)
        fence = []
        for p in group:
            for fence_pos, fdir in [(p + dir, dir) for dir in dir_list]:
                if not fence_pos.is_in_bounds(grid) or fence_pos.of_grid(grid) != val:
                    # assign each fence position a perpendicular direction so identical positions can be differentiated
                    check_dir = dir_list[(dir_list.index(fdir) + 1) % len(dir_list)]
                    fence.append((fence_pos, check_dir))

        # count all fences that don't have a neighbour in their direction
        fence_len = len(["" for f, fd in fence if (f + fd, fd) not in fence])
        result += len(group) * fence_len

    print(result)


if __name__ == "__main__":
    main()
