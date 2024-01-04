# AOC23 D17p1: Clumsy Crucible thanks to hyper-neutrino https://github.com/hyper-neutrino/advent-of-code/blob/main/2023/day17p1.py
from heapq import heappop, heappush


def main() -> None:
    with open("Day17\\input.txt") as f:
        city_map = f.read().splitlines()

    city_map = [list(map(int, line.strip())) for line in city_map]

    seen = set()
    #     hl, r, c,dr,dc, n - hl = heat loss, r = row index, c = columns index, dr = vertical direction, dc = horizzontal direction, n = number of step in same direction till last turn
    pq: list = [(0, 0, 0, 0, 0, 0)]

    while pq:
        hl, r, c, dr, dc, n = heappop(pq)

        if r == len(city_map) - 1 and c == len(city_map[0]) - 1:
            print(hl)
            break

        if (r, c, dr, dc, n) in seen:
            continue

        seen.add((r, c, dr, dc, n))

        if n < 3 and (dr, dc) != (0, 0):
            nr = r + dr
            nc = c + dc
            if 0 <= nr < len(city_map) and 0 <= nc < len(city_map[0]):
                heappush(pq, (hl + city_map[nr][nc], nr, nc, dr, dc, n + 1))

        for ndr, ndc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            if (ndr, ndc) != (dr, dc) and (ndr, ndc) != (-dr, -dc):
                nr = r + ndr
                nc = c + ndc
                if 0 <= nr < len(city_map) and 0 <= nc < len(city_map[0]):
                    heappush(pq, (hl + city_map[nr][nc], nr, nc, ndr, ndc, 1))


if __name__ == "__main__":
    main()
