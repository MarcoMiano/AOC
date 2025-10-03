# AOC24 D15p1: Warehouse Woes
import os
from dataclasses import dataclass


@dataclass
class Vec2:
    r: int = 0
    c: int = 0

    def __add__(self, other: "Vec2") -> "Vec2":
        return Vec2(self.r + other.r, self.c + other.c)


DIRS: dict[str, Vec2] = {
    "^": Vec2(-1, 0),
    ">": Vec2(0, 1),
    "v": Vec2(1, 0),
    "<": Vec2(0, -1),
}


@dataclass
class Warehouse:
    w_map: list[list[str]]
    pos: Vec2

    def move(self, inst: str) -> None:
        d: Vec2 = DIRS[inst]
        n = self.pos + d

        def see_next(m: Vec2) -> None | Vec2:
            match self.w_map[m.r][m.c]:
                case "#":
                    return None
                case "." | "@":
                    return m
                case "O":
                    return see_next(m + d)

        match self.w_map[n.r][n.c]:
            case "#":
                return
            case "." | "@":
                self.w_map[self.pos.r][self.pos.c] = "."
                self.pos = n
                self.w_map[n.r][n.c] = "@"
                return
            case "O":
                n1 = see_next(n + d)
                if n1 is not None:
                    self.w_map[self.pos.r][self.pos.c] = "."
                    self.pos = n
                    self.w_map[n.r][n.c] = "@"
                    self.w_map[n1.r][n1.c] = "O"
                return

    @property
    def gps(self) -> int:
        result = 0
        for r, row in enumerate(self.w_map):
            for c, char in enumerate(row):
                if char == "O":
                    result += 100 * r + c
        return result


def parse_input(input_path: str) -> tuple[Warehouse, str, Vec2]:
    with open(input_path) as file:
        raw_warehouse, raw_moves = file.read().split("\n\n")
    raw_warehouse = [list(lines) for lines in raw_warehouse.splitlines()]
    r, c = (0, 0)
    start_pos = None
    for r, row in enumerate(raw_warehouse):
        for c, char in enumerate(row):
            if char == "@":
                start_pos = Vec2(r, c)
                break
        if start_pos:
            break
    assert start_pos is not None
    return (
        Warehouse(raw_warehouse, start_pos),
        "".join(raw_moves.splitlines()),
        start_pos,
    )


def main() -> None:
    input_path: str = os.path.dirname(__file__) + "\\input.txt"
    warehouse, robot_moves, start_pos = parse_input(input_path)
    for inst in robot_moves:
        warehouse.move(inst)
    print(warehouse.gps)

    pass


if __name__ == "__main__":
    main()
