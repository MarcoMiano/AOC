# AOC24 D6p1: Guard Gallivant
import os


def parse_input(input_path):
    with open(input_path) as f:
        raw_map: list[str] = f.readlines()
    lab_map: list[list[str]] = [list(line) for line in raw_map]

    boundaries: tuple[int, int] = (len(lab_map[0]), len(lab_map))
    r_obstructions: dict[int, list[int]] = dict()
    c_obstructions: dict[int, list[int]] = dict()
    guard: str = ""
    guard_pos: tuple[int, int] = tuple()

    for r, row in enumerate(lab_map):
        for c, char in enumerate(row):
            if char == "#":
                if r not in r_obstructions.keys():
                    r_obstructions[r] = list()
                r_obstructions[r].append(c)

                if c not in c_obstructions.keys():
                    c_obstructions[c] = list()
                c_obstructions[c].append(r)
            elif char in "^>v<":
                guard = char
                guard_pos = (r, c)
            else:
                continue
    return r_obstructions, c_obstructions, guard, guard_pos, boundaries


def main() -> None:
    input_path: str = os.path.dirname(__file__) + "\\input.txt"
    r_obstructions, c_obstructions, guard, guard_pos, boundaries = parse_input(
        input_path
    )

    positions = set()
    positions.add(guard_pos)
    exit = False
    while not exit:
        if guard == "^":
            r_obs: list[int] = [
                item for item in c_obstructions[guard_pos[1]] if item < guard_pos[0]
            ]
            if not r_obs:
                r_ob = -1
                exit = True
            else:
                r_ob: int = max(r_obs)
            positions.update(
                {(pr, guard_pos[1]) for pr in range(r_ob + 1, guard_pos[0])}
            )
            guard_pos: tuple[int, int] = (r_ob + 1, guard_pos[1])
            guard = ">"

        elif guard == ">":
            c_obs: list[int] = [
                item for item in r_obstructions[guard_pos[0]] if item > guard_pos[1]
            ]
            if not c_obs:
                c_ob = boundaries[0]
                exit = True
            else:
                c_ob: int = min(c_obs)
            positions.update({(guard_pos[0], pc) for pc in range(guard_pos[1], c_ob)})
            guard_pos: tuple[int, int] = (guard_pos[0], c_ob - 1)
            guard = "v"

        elif guard == "v":
            r_obs: list[int] = [
                item for item in c_obstructions[guard_pos[1]] if item > guard_pos[0]
            ]
            if not r_obs:
                r_ob = boundaries[1]
                exit = True
            else:
                r_ob: int = min(r_obs)
            positions.update({(pr, guard_pos[1]) for pr in range(guard_pos[0], r_ob)})
            guard_pos: tuple[int, int] = (r_ob - 1, guard_pos[1])
            guard = "<"

        elif guard == "<":
            c_obs: list[int] = [
                item for item in r_obstructions[guard_pos[0]] if item < guard_pos[1]
            ]
            if not c_obs:
                c_ob = -1
                exit = True
            else:
                c_ob: int = max(c_obs)
            positions.update(
                {(guard_pos[0], pc) for pc in range(c_ob + 1, guard_pos[1])}
            )
            guard_pos: tuple[int, int] = (guard_pos[0], c_ob + 1)
            guard = "^"

        else:
            assert False, 'Unreacheable: guard is not in "^>v<"'

    print(len(positions))


if __name__ == "__main__":
    main()
