# AOC23 D14p2: Parabolic Reflector Dish

from copy import deepcopy


def get_load(platform: list[str]) -> int:
    columns_count: int = len(platform)
    mirrors_count: int = len(platform[0])

    platform_load: int = 0

    for i in range(columns_count):
        for j in range(mirrors_count):
            if platform[i][j] == "O":
                platform_load += mirrors_count - i

    return platform_load


def rewrite_column(column: str) -> str:
    segments: list[str] = column.split("#")
    new_column: list[str] = []
    for segment in segments:
        if not segment:
            if len(new_column) == len(column):
                break
            new_column.append("#")
            continue
        round_stone_count = segment.count("O")
        for i in range(len(segment)):
            new_column.append("." if i < len(segment) - round_stone_count else "O")
        if len(new_column) == len(column):
            break
        new_column.append("#")
    return "".join(new_column)


def spin_cycle(start_platform: list[str]) -> list[str]:
    platform: list[str] = start_platform
    for i in range(4):
        platform = list(zip(*platform[::-1]))
        platform = ["".join(line) for line in platform]

        new_platform = []
        for column in platform:
            new_platform.append(rewrite_column(column))
        platform = new_platform
    return platform


def get_hash(platform: list[str]) -> str:
    return "\n".join(["".join(line) for line in platform])


def main() -> None:
    with open("2023//Day14//input.txt") as f:
        platform = f.read().strip().splitlines()

    cycle_steps: dict[int, list[str]] = {}
    seen: dict[str, int] = {}
    ans_platform: list[str] = []

    for cycle in range(10**9):
        platform = spin_cycle(platform)

        platform_hash = get_hash(platform)
        if platform_hash in seen:
            period = cycle - seen[platform_hash]
            ans_platform = cycle_steps[
                (10**9 - 1 - seen[platform_hash]) % period + seen[platform_hash]
            ]
            break

        seen[platform_hash] = cycle
        cycle_steps[cycle] = deepcopy(platform)

    print(get_load(ans_platform))


if __name__ == "__main__":
    main()
