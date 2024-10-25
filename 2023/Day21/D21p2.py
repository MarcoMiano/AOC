# AOC23 D21p2: Step Counter
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
    def normalize_coordinate(coord, boundary):
        if coord < 0:
            while coord < 0:
                coord += boundary
        elif coord > boundary - 1:
            while coord > boundary - 1:
                coord -= boundary
        return coord

    row_count = len(garden_map)
    column_count = len(garden_map[0])
    new_positions = set()
    while positions:
        position = positions.pop()
        for direction in DIR.values():
            next_position = tuple(x + y for x, y in zip(position, direction))
            check_r = normalize_coordinate(next_position[0], row_count)
            check_c = normalize_coordinate(next_position[1], column_count)

            if garden_map[check_r][check_c] in ".S":
                new_positions.add((next_position))
    positions.update(new_positions)


def solve_quadratic(row_count: int, quadratic_gardens: list[int], steps: int):
    c = quadratic_gardens[0]
    b = (
        4 * quadratic_gardens[1] - 3 * quadratic_gardens[0] - quadratic_gardens[2]
    ) // 2
    a = quadratic_gardens[1] - quadratic_gardens[0] - b

    x = (steps - row_count // 2) // row_count
    return a * x**2 + b * x + c


def main() -> None:
    with open("Day21\\input.txt") as f:
        garden_map = f.read().strip().splitlines()
    positions = set()
    quadratic_steps = [65, 196, 327]
    quadratic_gardens: list[int] = list()
    for steps in quadratic_steps:
        positions = set()
        positions.add(find_starting_point(garden_map))
        for _ in range(steps):
            find_adjacent_gardens(garden_map, positions)
        quadratic_gardens.append(len(positions))
        print(f"In {steps} steps he can reach {len(positions)}")

    steps = 26501365
    print(solve_quadratic(len(garden_map), quadratic_gardens, steps))


if __name__ == "__main__":
    main()
