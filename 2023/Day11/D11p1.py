# AOC23 D11p1: Cosmic Expansion


def find_expanded_space(universe: list[str]) -> tuple[list[int], list[int]]:
    expanded_columns: list[int] = list()
    expanded_rows: list[int] = list()

    for r, row in enumerate(universe):
        if row.count(".") == row.__len__():
            expanded_rows.append(r)

    universe = list(zip(*universe[::-1]))

    for c, column in enumerate(universe):
        if column.count(".") == column.__len__():
            expanded_columns.append(c)

    return expanded_columns, expanded_rows


def find_galaxies(universe: list[str]) -> set[tuple[int, int]]:
    galaxies = set()

    for r, row in enumerate(universe):
        for c, char in enumerate(row):
            if char == "#":
                galaxies.add((r, c))

    return galaxies


def check_expansion(coord1: int, coord2: int, expanded_dimensions: list[int]) -> int:
    crossings: int = 0

    for expanded_dimension in expanded_dimensions:
        if min(coord1, coord2) < expanded_dimension < max(coord1, coord2):
            crossings += 1

    return crossings


def find_shortest_paths(
    galaxies: set[tuple[int, int]],
    expanded_columns: list[int],
    expanded_rows: list[int],
) -> int:
    shortest_paths = list()
    count: int = 0

    while len(galaxies) - 1 != 0:
        galaxy = galaxies.pop()

        for r, c in galaxies:
            shortest_paths.append(
                abs(galaxy[0] - r)
                + abs(galaxy[1] - c)
                + check_expansion(galaxy[0], r, expanded_rows)
                + check_expansion(galaxy[1], c, expanded_columns)
            )
            count += 1

    return sum(shortest_paths)


def main() -> None:
    with open("2023//Day11//input.txt") as f:
        universe = f.read().strip().splitlines()

    expanded_columns, expanded_rows = find_expanded_space(universe)

    galaxies = find_galaxies(universe)

    answer = find_shortest_paths(galaxies, expanded_columns, expanded_rows)

    print(answer)


if __name__ == "__main__":
    main()
