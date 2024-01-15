# AOC23 D22p1: Sand Slabs

from collections import defaultdict, deque
from dataclasses import dataclass
import queue
import numpy as np


@dataclass(frozen=True)
class Brick(object):
    corner1: tuple[int, int, int]
    corner2: tuple[int, int, int]

    def __lt__(self, other: "Brick") -> bool:
        return self.min_for_axis(2) < other.min_for_axis(2)

    def max_for_axis(self, axis: int) -> int:
        return max(self.corner1[axis], self.corner2[axis])

    def min_for_axis(self, axis: int) -> int:
        return min(self.corner1[axis], self.corner2[axis])

    def xy_area(self) -> tuple[tuple[int, int], tuple[int, int]]:
        return (
            (self.min_for_axis(0), self.min_for_axis(1)),
            (self.max_for_axis(0), self.max_for_axis(1)),
        )

    def height(self) -> int:
        return self.max_for_axis(2) - self.min_for_axis(2) + 1

    def area_intersecs(self, other: "Brick") -> bool:
        self_x1, self_y1 = self.xy_area()[0]
        self_x2, self_y2 = self.xy_area()[1]
        other_x1, other_y1 = other.xy_area()[0]
        other_x2, other_y2 = other.xy_area()[1]

        if self_x2 < other_x1 or other_x2 < self_x1:
            return False

        if self_y2 < other_y1 or other_y2 < self_y1:
            return False

        return True


def parse_bricks(data: list[str]) -> list[Brick]:
    bricks: list[Brick] = []
    for line in data:
        corner1, corner2 = line.split("~")
        (x1, y1, z1) = [int(val) for val in corner1.split(",")]
        (x2, y2, z2) = [int(val) for val in corner2.split(",")]
        bricks.append(Brick((x1, y1, z1), (x2, y2, z2)))

    return bricks


def find_upper_to_base_bricks(bricks: list[Brick]) -> dict[Brick, set]:
    bricks_at_level: dict[int, set[Brick]] = defaultdict(set)
    upper_to_base_bricks: dict[Brick, set[Brick]] = defaultdict(set)

    min_x = max_x = 0
    min_y = max_y = 0

    for brick in bricks:
        min_x = min(brick.min_for_axis(0), min_x)
        max_x = max(brick.min_for_axis(0), max_x)
        min_y = min(brick.min_for_axis(1), min_y)
        max_y = max(brick.min_for_axis(1), max_y)

    height_map = np.zeros((max_y - min_y + 1, max_x - min_x + 1), dtype=np.int32)

    for brick in bricks:
        (x1, y1), (x2, y2) = brick.xy_area()
        old_max_height = int(np.max(height_map[y1 : y2 + 1, x1 : x2 + 1]))
        new_max_height = old_max_height + brick.height()
        height_map[y1 : y2 + 1, x1 : x2 + 1] = new_max_height
        bricks_at_level[new_max_height].add(brick)

        upper_to_base_bricks[brick].update(
            base_brick
            for base_brick in bricks_at_level[old_max_height]
            if base_brick.area_intersecs(brick)
        )
    return upper_to_base_bricks


def find_base_to_upper_bricks(
    bricks: list[Brick], upper_to_base_bricks: dict[Brick, set]
) -> dict[Brick, set]:
    base_to_upper_bricks = {brick: set() for brick in bricks}

    for brick in bricks:
        for base_brick in upper_to_base_bricks[brick]:
            base_to_upper_bricks[base_brick].add(brick)
    return base_to_upper_bricks


def main() -> None:
    with open("Day22\\input.txt") as f:
        snapshot = f.read().strip().splitlines()
    bricks: list[Brick] = parse_bricks(snapshot)
    bricks.sort()

    upper_to_base_bricks = find_upper_to_base_bricks(bricks)
    base_to_upper_bricks = find_base_to_upper_bricks(bricks, upper_to_base_bricks)

    total_falling_bricks = 0

    for brick in upper_to_base_bricks:
        queue = deque(
            upper
            for upper in base_to_upper_bricks[brick]
            if len(upper_to_base_bricks[upper]) == 1
        )
        falling = set(queue)
        falling.add(brick)

        while queue:
            upper = queue.popleft()

            for base in base_to_upper_bricks[upper] - falling:
                if upper_to_base_bricks[base] < falling:
                    queue.append(base)
                    falling.add(base)

        total_falling_bricks += len(falling) - 1

    print(total_falling_bricks)


if __name__ == "__main__":
    main()
