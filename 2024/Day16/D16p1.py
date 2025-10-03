# AOC24 D16p1: Reindeer Maze
import os
import heapq
from dataclasses import dataclass


@dataclass(frozen=True)
class Vec2:
    r: int = 0
    c: int = 0

    def __add__(self, other: "Vec2") -> "Vec2":
        return Vec2(self.r + other.r, self.c + other.c)


NORTH = Vec2(-1, 0)
EAST = Vec2(0, 1)
SOUTH = Vec2(1, 0)
WEST = Vec2(0, -1)

ROT_LEFT: dict[Vec2, Vec2] = {NORTH: WEST, WEST: SOUTH, SOUTH: EAST, EAST: NORTH}
ROT_RIGHT: dict[Vec2, Vec2] = {NORTH: EAST, EAST: SOUTH, SOUTH: WEST, WEST: NORTH}

DIRS: dict[str, Vec2] = {
    "N": NORTH,
    "E": EAST,
    "S": SOUTH,
    "W": WEST,
}

INF = float("inf")


def parse_input(
    input_path: str,
) -> tuple[list[list[str]], tuple[int, int]]:
    text = open(input_path).read()
    result: list[list[str]] = []
    start: tuple[int, int] = (0, 0)
    for r, line in enumerate(text.splitlines()):
        if start == (0, 0):
            start_col = line.find("S")
            if start_col != -1:
                start = (r, start_col)

        result.append(list(line))
    return result, start


def dijkstra(maze: list[list[str]], start: tuple[int, int], d: str) -> int:
    goal = Vec2()
    for r, row in enumerate(maze):
        for c, char in enumerate(row):
            if char == "E":
                goal = Vec2(r, c)
                break

    start_vec = Vec2(*start)
    dist = dict()
    start_state: tuple[Vec2, Vec2] = (start_vec, DIRS[d])
    dist[start_state] = 0

    pq: list[tuple[int, int, Vec2, Vec2]] = []
    tie = 0
    heapq.heappush(pq, (0, tie, start_vec, DIRS[d]))

    while pq:
        cost, _, pos, heading = heapq.heappop(pq)

        if cost != dist.get((pos, heading), INF):
            continue

        if pos == goal:
            return cost

        nl: tuple[Vec2, Vec2] = (pos, ROT_LEFT[heading])
        nc: int = cost + 1000
        if nc < dist.get(nl, INF):
            dist[nl] = nc
            tie += 1
            heapq.heappush(pq, (nc, tie, nl[0], nl[1]))

        nr: tuple[Vec2, Vec2] = (pos, ROT_RIGHT[heading])
        nc = cost + 1000
        if nc < dist.get(nr, INF):
            dist[nr] = nc
            tie += 1
            heapq.heappush(pq, (nc, tie, nr[0], nr[1]))

        fpos = pos + heading
        if maze[fpos.r][fpos.c] != "#":
            nf = (fpos, heading)
            nc = cost + 1
            if nc < dist.get(nf, INF):
                dist[nf] = nc
                tie += 1
                heapq.heappush(pq, (nc, tie, nf[0], nf[1]))

    return -1


def main() -> None:
    input_path: str = os.path.dirname(__file__) + "\\input.txt"
    maze, start = parse_input(input_path)
    print(dijkstra(maze, start, "E"))


if __name__ == "__main__":
    main()
