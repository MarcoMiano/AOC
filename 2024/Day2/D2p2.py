# AOC24 D2p1: Red-Nosed Reports

import os

from itertools import pairwise


def parse_input(input_path) -> list[list[int]]:
    reports: list[list[int]] = list()
    with open(input_path) as f:
        raw_input: list[str] = f.readlines()

    reports = [[int(data) for data in line.split()] for line in raw_input]

    return reports


def is_sorted(l: list) -> bool:
    return all(a < b for a, b in pairwise(l)) or all(a > b for a, b in pairwise(l))


def is_step_limited(l: list) -> bool:
    return all(0 < abs(a - b) < 4 for a, b in pairwise(l))


def main() -> None:
    input_path: str = os.path.dirname(__file__) + "\\input.txt"
    reports: list[list[int]] = parse_input(input_path)

    safe_count = 0
    for report in reports:
        if is_sorted(report) and is_step_limited(report):
            safe_count += 1
            continue

        for i, _ in enumerate(report):
            mod_report: list[int] = [x for j, x in enumerate(report) if j != i]

            if is_sorted(mod_report) and is_step_limited(mod_report):
                safe_count += 1
                break

    print(safe_count)


if __name__ == "__main__":
    main()
