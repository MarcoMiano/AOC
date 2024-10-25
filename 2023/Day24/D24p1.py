# AOC23 D24p1: Never Tell Me The Odds
from dataclasses import dataclass
from typing import TypeAlias
from pprint import pprint

CHECK_AREA: dict[str, int] = {"min": 200000000000000, "max": 400000000000000}


@dataclass()
class Hail:
    px0: int
    py0: int
    pz0: int
    vx: int
    vy: int
    vz: int


t_collisions: TypeAlias = list[tuple[Hail, Hail, tuple[float, float]]]


def load_hails(file_path: str) -> list[Hail]:
    hails: list[Hail] = list()
    with open(file_path) as f:
        lines: list[str] = f.read().splitlines()
        for line in lines:
            pos, vel = line.split("@")
            pos = [int(p) for p in pos.split(", ")]
            vel = [int(v) for v in vel.split(", ")]
            hails.append(
                Hail(
                    px0=pos[0], py0=pos[1], pz0=pos[2], vx=vel[0], vy=vel[1], vz=vel[2]
                )
            )
    return hails


def find_intersection_2D(hails: list[Hail]) -> t_collisions:
    collisions = list()
    done = set()
    for h1, hail1 in enumerate(hails):
        for h2, hail2 in enumerate(hails):
            if h1 == h2:
                continue
            if (h2, h1) in done:
                continue

            done.add((h1, h2))

            k1: float = hail1.vy / hail1.vx
            k2: float = hail2.vy / hail2.vx

            if k1 == k2 and hail1.px0 != hail2.px0:
                continue
            if k1 == k2 and hail1.py0 != hail2.py0:
                continue
            # if k1 == k2 and hail1.pz0 != hail2.pz0:
            #     continue

            c1: float = hail1.py0 - (k1 * hail1.px0)
            c2: float = hail2.py0 - (k2 * hail2.px0)

            x: float = (c2 - c1) / (k1 - k2)
            y: float = c1 + k1 * x

            tx1: float = (x - hail1.px0) / hail1.vx
            ty1: float = (y - hail1.py0) / hail1.vy
            tx2: float = (x - hail2.px0) / hail2.vx
            ty2: float = (y - hail2.py0) / hail2.vy

            if (
                (tx1 >= 0 and ty1 >= 0 and tx2 >= 0 and ty2 >= 0)
                and CHECK_AREA["min"] < x < CHECK_AREA["max"]
                and CHECK_AREA["min"] < y < CHECK_AREA["max"]
            ):
                collisions.append((hail1, hail2, (x, y)))
    return collisions


# collision x at tx = (A.px0 - B.px0)/(A.vx - B.vx)
# collision y at ty = (A.py0 - B.py0)/(A.vy - B.vy)
# collision z at tz = (A.pz0 - B.pz0)/(A.vz - B.vz)
# if tx = ty = tz a collision will happen at t = tx = ty = tz
# collision position at x = A.px0 + A.vx * t
def main() -> None:
    hails: list[Hail] = load_hails("2023//Day24//input.txt")
    pprint(hails)
    collisions: t_collisions = find_intersection_2D(hails)

    print(len(collisions))


if __name__ == "__main__":
    main()
