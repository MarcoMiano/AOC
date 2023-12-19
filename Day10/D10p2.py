# AOC23 D10p2: Pipe Maze thanks to hyper-neutrino https://github.com/hyper-neutrino/advent-of-code/blob/main/2023/day10p2.py
from collections import deque


def find_starting_point(maze: list[str]) -> tuple[int, int]:
    for r, row in enumerate(maze):
        for c, char in enumerate(row):
            if char == "S":
                return (r, c)
    return (-1, -1)


def find_loop(
    maze: list[str], start_coords: tuple[int, int]
) -> tuple[set[tuple[int, int]], str]:
    starting_point_list = {"|", "-", "J", "L", "7", "F"}

    loop = {start_coords}
    loop_queue = deque([start_coords])

    while loop_queue:
        r, c = loop_queue.popleft()
        char = maze[r][c]

        if (
            r > 0
            and char in "S|LJ"
            and maze[r - 1][c] in "|7F"
            and (r - 1, c) not in loop
        ):  # UP
            loop.add((r - 1, c))
            loop_queue.append((r - 1, c))
            if char == "S":
                starting_point_list &= {"|", "J", "L"}

        if (
            r < len(maze) - 1
            and char in "S|7F"
            and maze[r + 1][c] in "|LJ"
            and (r + 1, c) not in loop
        ):  # DOWN
            loop.add((r + 1, c))
            loop_queue.append((r + 1, c))
            if char == "S":
                starting_point_list &= {"|", "7", "F"}

        if (
            c > 0
            and char in "S-J7"
            and maze[r][c - 1] in "-LF"
            and (r, c - 1) not in loop
        ):  # LEFT
            loop.add((r, c - 1))
            loop_queue.append((r, c - 1))
            if char == "S":
                starting_point_list &= {"-", "J", "7"}

        if (
            c < len(maze[r]) - 1
            and char in "S-LF"
            and maze[r][c + 1] in "-J7"
            and (r, c + 1) not in loop
        ):  # RIGHT
            loop.add((r, c + 1))
            loop_queue.append((r, c + 1))
            if char == "S":
                starting_point_list &= {"-", "L", "F"}
    assert len(starting_point_list) == 1
    starting_point_char = "".join(list(starting_point_list))
    return loop, starting_point_char


def clean_maze(maze: list[str], loop: set[tuple[int, int]]) -> list[str]:
    return [
        "".join(char if (r, c) in loop else "." for c, char in enumerate(row))
        for r, row in enumerate(maze)
    ]


def outside_tiles(maze: list[str]) -> set[tuple[int, int]]:
    outside = set()

    for r, row in enumerate(maze):
        inside_maze: bool = False
        facing_up: bool | None = None
        for c, char in enumerate(row):
            if char == "|":
                assert facing_up is None
                inside_maze = not inside_maze
            elif char == "-":
                assert facing_up is not None
            elif char in "LF":
                assert facing_up is None
                facing_up = char == "L"
            elif char in "7J":
                assert facing_up is not None
                if char != ("J" if facing_up else "7"):
                    inside_maze = not inside_maze
                facing_up = None
            elif char == ".":
                pass
            else:
                raise RuntimeError(f"Unexpected character (horizontal): {char}")
            if not inside_maze:
                outside.add((r, c))

    return outside


def main() -> None:
    with open("Day10\\input.txt") as f:
        maze: list[str] = f.read().strip().splitlines()

    start_coords = find_starting_point(maze)
    assert start_coords != (-1, -1)

    loop, starting_point_char = find_loop(maze, start_coords)

    maze[start_coords[0]] = maze[start_coords[0]].replace("S", starting_point_char)

    maze = clean_maze(maze, loop)

    outside_maze = outside_tiles(maze)

    print(len(maze) * len(maze[0]) - len(outside_maze | loop))

    return


if __name__ == "__main__":
    main()
