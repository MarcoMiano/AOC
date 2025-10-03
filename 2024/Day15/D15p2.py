# AOC24 D15p2: Warehouse Woes
import os
from dataclasses import dataclass


@dataclass(frozen=True)
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

EXPAND: dict[str, str] = {
    "#": "##",
    "O": "[]",
    ".": "..",
    "@": "@.",
}


@dataclass
class Warehouse:
    w_map: list[list[str]]
    pos: Vec2

    def _left_of(self, v: Vec2) -> Vec2:
        char = self._w_map(v)
        if char == "[":
            return v
        if char == "]":
            return Vec2(v.r, v.c - 1)
        raise ValueError(f"_left_of called on a non box tile at {v} ({char!r})")

    def _collect_vertical_push(self, d: Vec2, start: Vec2) -> set[Vec2] | None:
        start_left = self._left_of(start)
        queue: list[Vec2] = [start_left]
        seen: set[Vec2] = set()
        to_move: set[Vec2] = set()

        while queue:
            left: Vec2 = queue.pop()
            if left in seen:
                continue
            seen.add(left)
            to_move.add(left)

            up1 = left + d
            up2 = left + DIRS[">"] + d

            s1, s2 = self._w_map(up1), self._w_map(up2)
            if s1 == "#" or s2 == "#":
                return None
            if s1 in "[]":
                queue.append(self._left_of(up1))
            if s2 in "[]":
                queue.append(self._left_of(up2))

        return to_move

    def _push_horizontal(self, d: Vec2, n: Vec2) -> bool:
        cur: Vec2 = n
        while self._w_map(cur) in "[]":
            cur = cur + d
        if self._w_map(cur) == "#":
            return False

        back = Vec2(-d.r, -d.c)
        while cur != n:
            prev = cur + back
            self._set(cur, self._w_map(prev))
            cur = prev
        self._set(n, ".")
        return True

    def _push_vertical(self, d: Vec2, n: Vec2) -> bool:
        to_move = self._collect_vertical_push(d, n)
        if to_move is None:
            return False

        for left in to_move:
            self._set(left, ".")
            self._set(Vec2(left.r, left.c + 1), ".")
        for left in to_move:
            dest: Vec2 = left + d
            self._set(dest, "[")
            self._set(Vec2(dest.r, dest.c + 1), "]")

        return True

    def _set(self, v: Vec2, char: str) -> None:
        self.w_map[v.r][v.c] = char

    def _w_map(self, v: Vec2) -> str:
        return self.w_map[v.r][v.c]

    def move(self, inst: str) -> None:
        d: Vec2 = DIRS[inst]
        n: Vec2 = self.pos + d

        char = self._w_map(n)
        if char == "#":
            return
        if char == ".":
            self._set(self.pos, ".")
            self.pos = n
            self._set(self.pos, "@")
            return

        pushed: bool = False
        if inst in "<>":
            pushed = self._push_horizontal(d, n)
        else:
            pushed = self._push_vertical(d, n)

        if pushed:
            self._set(self.pos, ".")
            self.pos = n
            self._set(self.pos, "@")

    @property
    def gps(self) -> int:
        result = 0
        for r, row in enumerate(self.w_map):
            for c, char in enumerate(row):
                if char == "[":
                    result += 100 * r + c
        return result


def parse_input(input_path: str) -> tuple[Warehouse, str]:
    with open(input_path) as file:
        raw_warehouse, raw_moves = file.read().split("\n\n")
    exp_warehouse: list[list[str]] = []
    start_pos = None
    for r, line in enumerate(raw_warehouse.splitlines()):
        exp_row = "".join(EXPAND[char] for char in line)
        c = exp_row.find("@")
        if c != -1:
            start_pos = Vec2(r, c)
        exp_warehouse.append(list(exp_row))

    assert start_pos is not None
    return Warehouse(exp_warehouse, start_pos), "".join(raw_moves.splitlines())


def main() -> None:
    input_path: str = os.path.dirname(__file__) + "\\input.txt"
    warehouse, robot_moves = parse_input(input_path)
    for inst in robot_moves:
        warehouse.move(inst)

    print(warehouse.gps)

    pass


if __name__ == "__main__":
    main()
