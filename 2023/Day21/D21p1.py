# AOC23 D21p1: Step Counter
DIR = {"U": (-1, 0), "R": (0, 1), "D": (1, 0), "L": (0, -1)}


def find_starting_point(garden_map: list[str]) -> tuple[int, int]:
    for r, row in enumerate(garden_map):
        for c, char in enumerate(row):
            if char == "S":
                return (r, c)
    return (-1, -1)


def find_adjacent_gardens(
    garden_map: list[str], positions: set[tuple[int, int]]
) -> None:
    row_count = len(garden_map)
    column_count = len(garden_map[0])
    new_positions = set()
    while positions:
        position = positions.pop()
        for direction in DIR.values():
            next_position = tuple(x + y for x, y in zip(position, direction))
            check_boundaries = (
                next_position[0] >= 0
                and next_position[0] < row_count
                and next_position[1] >= 0
                and next_position[1] < column_count
            )
            if (
                garden_map[next_position[0]][next_position[1]] in ".S"
                and check_boundaries
            ):  # Move up
                new_positions.add((next_position))
    positions.update(new_positions)


def main() -> None:
    with open("Day21\\input.txt") as f:
        garden_map = f.read().strip().splitlines()
    positions = set()
    positions.add(find_starting_point(garden_map))

    for _ in range(64):
        find_adjacent_gardens(garden_map, positions)
    print(len(positions))


if __name__ == "__main__":
    main()
