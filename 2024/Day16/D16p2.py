# AOC24 D16p2: Reindeer Maze
import os
import heapq
from dataclasses import dataclass
from collections import deque


@dataclass(frozen=True)
class Vec2:
    r: int = 0
    c: int = 0

    def __add__(self, other: "Vec2") -> "Vec2":
        return Vec2(self.r + other.r, self.c + other.c)

    def __sub__(self, other: "Vec2") -> "Vec2":
        return Vec2(self.r - other.r, self.c - other.c)


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

INF = 999_999_999


def parse_input(
    input_path: str,
) -> tuple[list[list[str]], Vec2]:
    text = open(input_path).read()
    result: list[list[str]] = []
    start = Vec2()
    for r, line in enumerate(text.splitlines()):
        if start == Vec2(0, 0):
            start_col = line.find("S")
            if start_col != -1:
                start = Vec2(r, start_col)

        result.append(list(line))
    return result, start


def dijkstra_forward(
    maze: list[list[str]], start: Vec2, d: str
) -> tuple[dict[tuple[Vec2, Vec2], int], int, Vec2]:
    goal = Vec2()
    for r, row in enumerate(maze):
        for c, char in enumerate(row):
            if char == "E":
                goal = Vec2(r, c)
                break

    dist = dict()
    start_state: tuple[Vec2, Vec2] = (start, DIRS[d])
    dist[start_state] = 0

    pq: list[tuple[int, int, Vec2, Vec2]] = []
    tie = 0
    heapq.heappush(pq, (0, tie, start, DIRS[d]))
    best_cost: int = INF

    while pq:
        cost, _, pos, heading = heapq.heappop(pq)

        if cost != dist.get((pos, heading), INF):
            continue

        if pos == goal:
            best_cost = min(best_cost, cost)

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

    return dist, best_cost, goal


def dijkstra_reverse(maze: list[list[str]], goal: Vec2) -> dict[tuple[Vec2, Vec2], int]:
    dist: dict[tuple[Vec2, Vec2], int] = dict()
    pq: list[tuple[int, int, Vec2, Vec2]] = []
    tie = 0

    for h in [NORTH, EAST, SOUTH, WEST]:
        s = (goal, h)
        dist[s] = 0
        heapq.heappush(pq, (0, tie, goal, h))
        tie += 1

    while pq:
        cost, _, pos, heading = heapq.heappop(pq)
        if cost != dist.get((pos, heading), INF):
            continue

        pred = (pos, ROT_RIGHT[heading])
        nc = cost + 1000
        if nc < dist.get(pred, INF):
            dist[pred] = nc
            tie += 1
            heapq.heappush(pq, (nc, tie, pred[0], pred[1]))

        pred = (pos, ROT_LEFT[heading])
        nc = cost + 1000
        if nc < dist.get(pred, INF):
            dist[pred] = nc
            tie += 1
            heapq.heappush(pq, (nc, tie, pred[0], pred[1]))

        back = pos - heading
        if maze[back.r][back.c] != "#" and maze[pos.r][pos.c] != "#":
            pred = (back, heading)
            nc = cost + 1
            if nc < dist.get(pred, INF):
                dist[pred] = nc
                tie += 1
                heapq.heappush(pq, (nc, tie, pred[0], pred[1]))
    return dist


def main() -> None:
    input_path: str = os.path.dirname(__file__) + "\\input.txt"
    maze, start = parse_input(input_path)
    dist_f, best_cost, goal = dijkstra_forward(maze, start, "E")
    dist_r = dijkstra_reverse(maze, goal)

    start_state = (start, DIRS["E"])

    def gen_neighbors(pos, heading):
        yield (pos, ROT_LEFT[heading], 1000)
        yield (pos, ROT_RIGHT[heading], 1000)
        fpos = pos + heading
        if maze[fpos.r][fpos.c] != "#":
            yield (fpos, heading, 1)

    q = deque([start_state])
    seen_states = {start_state}

    while q:
        pos, heading = q.popleft()
        for npos, nhead, w in gen_neighbors(pos, heading):
            s = (pos, heading)
            t = (npos, nhead)
            df = dist_f.get(s)
            dr = dist_r.get(t)

            if df is None or dr is None:
                continue
            if df + w + dr == best_cost:
                if t not in seen_states:
                    seen_states.add(t)
                    q.append(t)

    tiles_on_optimal = {
        pos for (pos, _h) in seen_states if dist_r.get((pos, _h), None) is not None
    }
    count = len({p for p in tiles_on_optimal})
    print(count)


if __name__ == "__main__":
    main()
