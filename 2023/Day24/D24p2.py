# AOC23 D24p1: Never Tell Me The Odds
from typing import TypeAlias
import sympy
from pprint import pprint

CHECK_AREA: dict[str, int] = {"min": 200000000000000, "max": 400000000000000}

t_hail: TypeAlias = list[list[int]]


def load_hails(file_path: str) -> t_hail:
    hails: t_hail = list()
    with open(file_path) as f:
        lines: list[str] = f.read().splitlines()
        for line in lines:
            hails.append([int(l) for l in line.replace(" @ ", ", ").split(", ")])
    return hails


def main() -> None:
    hails: t_hail = load_hails("2023//Day24//input.txt")
    xr, yr, zr, vxr, vyr, vzr = sympy.symbols("xr, yr, zr, vxr, vyr, vzr")
    print(xr)

    equations = []

    for i, [x, y, z, vx, vy, vz] in enumerate(hails):
        equations.append((xr - x) * (vy - vyr) - (yr - y) * (vx - vxr))
        equations.append((yr - y) * (vz - vzr) - (zr - z) * (vy - vyr))
        print(f"{i}, {len(equations)}")
        if len(equations) < 6:
            continue
        answer = sympy.solve(equations)
        if len(answer) == 1:
            answer = answer[0]
            break
    print(answer[xr] + answer[yr] + answer[zr])


if __name__ == "__main__":
    main()
