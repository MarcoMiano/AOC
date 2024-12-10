# AOC24 D6p2: Guard Gallivant
import os

NEXT_DIRECTION = {"^": ">", ">": "v", "v": "<", "<": "^"}
DIRECTIONS: dict[str, tuple[int, int]] = {
    "^": (-1, 0),
    ">": (0, 1),
    "v": (1, 0),
    "<": (0, -1),
}


def parse_input(input_path):
    with open(input_path) as f:
        raw_map: list[str] = f.readlines()
    lab_map: list[list[str]] = [list(line) for line in raw_map]

    boundaries: tuple[int, int] = (len(lab_map), len(lab_map[0]))
    r_obs: dict[int, list[int]] = dict()
    c_obs: dict[int, list[int]] = dict()
    obstructions: set[tuple[int, int]] = set()
    guard: str = ""
    guard_pos: tuple[int, int] = tuple()

    for r, row in enumerate(lab_map):
        if r not in r_obs.keys():
            r_obs[r] = list()
        for c, char in enumerate(row):
            if c not in c_obs.keys():
                c_obs[c] = list()
            if char == "#":
                obstructions.add((r, c))
                r_obs[r].append(c)
                c_obs[c].append(r)
            elif char in "^>v<":
                guard = char
                guard_pos = (r, c)
            else:
                continue
    return obstructions, guard, guard_pos, boundaries


def check_loop(
    pos: tuple[int, int],
    direction: str,
    r_obs: dict[int, list[int]],
    c_obs: dict[int, list[int]],
    hitted_obs: dict[tuple[int, int], set[str]],
) -> bool:
    if NEXT_DIRECTION[direction] == "^":
        r: list[int] = [r for r in c_obs[pos[1]] if r < pos[0]]
        if not r:
            return False
        obs: tuple[int, int] = (max(r), pos[1])
        if obs in hitted_obs.keys() and "^" in hitted_obs[obs]:
            return True
    elif NEXT_DIRECTION[direction] == ">":
        c: list[int] = [c for c in r_obs[pos[0]] if c > pos[1]]
        if not c:
            return False
        obs = (pos[0], min(c))
        if obs in hitted_obs.keys() and ">" in hitted_obs[obs]:
            return True
    elif NEXT_DIRECTION[direction] == "v":
        r = [r for r in c_obs[pos[1]] if r > pos[0]]
        if not r:
            return False
        obs = (min(r), pos[1])
        if obs in hitted_obs.keys() and "v" in hitted_obs[obs]:
            return True
    elif NEXT_DIRECTION[direction] == "<":
        c = [c for c in r_obs[pos[0]] if c < pos[1]]
        if not c:
            return False
        obs = (pos[0], max(c))
        if obs in hitted_obs.keys() and "<" in hitted_obs[obs]:
            return True
    return False


def sim_guard(
    obstructions: set[tuple[int, int]],
    guard_dir: str,
    guard_position: tuple[int, int],
    boundaries: tuple[int, int],
    loop: bool = False,
) -> int:
    guard = guard_dir
    guard_pos = guard_position
    hitted_obs: dict[tuple[int, int], set[str]] = {key: set() for key in obstructions}
    new_obstructions = set()
    positions = set()
    exit = False

    i = 0

    while not exit:
        if guard not in "^>v<":
            assert False, "Guard not in '^>v<'"
        next_pos: tuple[int, int] = (
            guard_pos[0] + DIRECTIONS[guard][0],
            guard_pos[1] + DIRECTIONS[guard][1],
        )
        if not (0 <= next_pos[0] < boundaries[0]) or not (
            0 <= next_pos[1] < boundaries[1]
        ):
            exit = True
            i = 0
            continue

        if next_pos in obstructions:
            hitted_obs[next_pos].add(guard)
            guard = NEXT_DIRECTION[guard]
            continue

        if not loop:
            new_obstruction = (
                next_pos[0] + DIRECTIONS[guard][0],
                next_pos[1] + DIRECTIONS[guard][1],
            )
            if not (0 <= new_obstruction[0] < boundaries[0]) or not (
                0 <= new_obstruction[1] < boundaries[1]
            ):
                exit = True
                i = 0
                continue
            if (
                sim_guard(
                    obstructions.union({new_obstruction}),
                    guard_dir,
                    guard_position,
                    boundaries,
                    True,
                )
                == -1
            ):
                # print(f"new_obstruction: {new_obstruction}")
                new_obstructions.add(new_obstruction)

        if loop:
            if next_pos in positions:
                i += 1

        if loop and i > 100:
            return -1

        guard_pos: tuple[int, int] = next_pos
        positions.add(guard_pos)
    return len(new_obstructions)


def main() -> None:
    input_path: str = os.path.dirname(__file__) + "\\input.txt"

    result: int = sim_guard(*parse_input(input_path))
    print(result)


if __name__ == "__main__":
    main()
