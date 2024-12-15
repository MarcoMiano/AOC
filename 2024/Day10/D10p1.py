# AOC24 D10p1: Hoof It
import os

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def parse_input(input_path: str) -> list[list[int]]:
    with open(input_path, "r") as f:
        raw_map: list[str] = f.read().strip().splitlines()
    topographic_map: list[list[int]] = [[int(c) for c in line] for line in raw_map]
    return topographic_map


def calc_score(trailhead: tuple[int, int], topo_map: list[list[int]]) -> int:
    def in_bounds(tr, tc) -> bool:
        return 0 <= tr < len(topo_map) and 0 <= tc < len(topo_map[0])

    next_tiles = [trailhead]
    seen = {trailhead}
    ends = 0
    while next_tiles:
        r, c = next_tiles.pop()
        seen.add((r, c))

        if topo_map[r][c] == 9:
            ends += 1
            continue

        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if not in_bounds(nr, nc):
                continue
            if (nr, nc) in seen:
                continue
            if topo_map[nr][nc] == topo_map[r][c] + 1:
                next_tiles.append((nr, nc))

    return ends


def main() -> None:
    input_path: str = os.path.dirname(__file__) + "\\input.txt"
    topo_map: list[list[int]] = parse_input(input_path)

    result = 0
    for r, row in enumerate(topo_map):
        for c, char in enumerate(row):
            if char == 0:
                result += calc_score((r, c), topo_map)

    print(result)


if __name__ == "__main__":
    main()
