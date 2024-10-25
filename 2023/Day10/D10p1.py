# AOC23 D10p1: Pipe Maze thanks to hyper-neutrino https://github.com/hyper-neutrino/advent-of-code/blob/main/2023/day10p1.py
from collections import deque


def find_starting_point(maze: list[str]) -> tuple[int, int]:
    for r, row in enumerate(maze):
        for c, char in enumerate(row):
            if char == "S":
                return (r, c)
    return (-1, -1)


def find_loop(
    maze: list[str], start_coordinates: tuple[int, int]
) -> set[tuple[int, int]]:
    loop = {start_coordinates}
    loop_queue = deque([start_coordinates])

    while loop_queue:
        r, c = loop_queue.popleft()
        char = maze[r][c]

        if (
            r > 0
            and char in "S|LJ"
            and maze[r - 1][c] in "|7F"
            and (r - 1, c) not in loop
        ):
            loop.add((r - 1, c))
            loop_queue.append((r - 1, c))

        if (
            r < len(maze) - 1
            and char in "S|7F"
            and maze[r + 1][c] in "|LJ"
            and (r + 1, c) not in loop
        ):
            loop.add((r + 1, c))
            loop_queue.append((r + 1, c))

        if (
            c > 0
            and char in "S-J7"
            and maze[r][c - 1] in "-LF"
            and (r, c - 1) not in loop
        ):
            loop.add((r, c - 1))
            loop_queue.append((r, c - 1))

        if (
            c < len(maze[r]) - 1
            and char in "S-LF"
            and maze[r][c + 1] in "-J7"
            and (r, c + 1) not in loop
        ):
            loop.add((r, c + 1))
            loop_queue.append((r, c + 1))
    return loop


def main() -> None:
    with open("2023//Day10//input.txt") as f:
        maze: list[str] = f.read().strip().splitlines()

    start_coordinates = find_starting_point(maze)
    assert start_coordinates != (-1, -1)

    loop = find_loop(maze, start_coordinates)

    print(len(loop) // 2)
    return


if __name__ == "__main__":
    main()
