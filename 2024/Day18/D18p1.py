# AOC24 D18p1: RAM Run
import os
import heapq
from dataclasses import dataclass
from pprint import pprint


@dataclass(frozen=True)
class Vec2:
    r: int = 0
    c: int = 0

    def __add__(self, other: "Vec2") -> "Vec2":
        return Vec2(self.r + other.r, self.c + other.c)

    def inside(self, low: "Vec2", high: "Vec2", inclusive: bool = False) -> bool:
        lr, hr = sorted((low.r, high.r))
        lc, hc = sorted((low.c, high.c))
        if inclusive:
            return (lr <= self.r <= hr) and (lc <= self.c <= hc)
        else:
            return (lr <= self.r < hr) and (lc <= self.c < hc)


MAZE_DIM = Vec2(71, 71)

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
) -> list[Vec2]:
    inst: list[Vec2] = list()
    lines = open(input_path).readlines()
    for line in lines:
        inst.append(Vec2(*map(int, line.split(","))))
    return inst


def simulate(inst: list[Vec2], cycles: int) -> list[list[str]]:
    maze = [["." for c in range(MAZE_DIM.c)] for r in range(MAZE_DIM.r)]
    i = 0
    while i < cycles:
        coord = inst[i]
        maze[coord.c][coord.r] = "#"
        i += 1
    return maze


def dijkstra(maze: list[list[str]], start: Vec2, goal: Vec2) -> int:
    d = "E"
    dist = dict()
    start_state: tuple[Vec2, Vec2] = (start, DIRS[d])
    dist[start_state] = 0

    pq: list[tuple[int, int, Vec2, Vec2]] = []
    tie = 0
    heapq.heappush(pq, (0, tie, start, DIRS[d]))

    while pq:
        cost, _, pos, heading = heapq.heappop(pq)

        if cost != dist.get((pos, heading), INF):
            continue

        if pos == goal:
            return cost

        nl: tuple[Vec2, Vec2] = (pos, ROT_LEFT[heading])
        nc: int = cost
        if nc < dist.get(nl, INF):
            dist[nl] = nc
            tie += 1
            heapq.heappush(pq, (nc, tie, nl[0], nl[1]))

        nr: tuple[Vec2, Vec2] = (pos, ROT_RIGHT[heading])
        # nc = cost + 1
        if nc < dist.get(nr, INF):
            dist[nr] = nc
            tie += 1
            heapq.heappush(pq, (nc, tie, nr[0], nr[1]))

        fpos = pos + heading
        if not fpos.inside(Vec2(0, 0), MAZE_DIM):
            continue
        if maze[fpos.r][fpos.c] != "#":
            nf: tuple[Vec2, Vec2] = (fpos, heading)
            nc: int = cost + 1
            if nc < dist.get(nf, INF):
                dist[nf] = nc
                tie += 1
                heapq.heappush(pq, (nc, tie, nf[0], nf[1]))

    return -1


def main() -> None:
    input_path: str = os.path.dirname(__file__) + "\\input.txt"
    inst: list[Vec2] = parse_input(input_path)
    maze: list[list[str]] = simulate(inst, 1024)
    pprint(maze)
    start = Vec2(0, 0)
    goal = Vec2(70, 70)
    print(dijkstra(maze, start, goal))


if __name__ == "__main__":
    main()
