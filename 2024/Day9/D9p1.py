# AOC24 D9p1: Disk Fragmenter
import os

from itertools import zip_longest


def parse_input(input_path: str) -> list[str]:
    with open(input_path, "r") as f:
        disk_map: str = f.read()
    disk = list()
    file_id = 0
    for file_len, free_len in zip_longest(disk_map[::2], disk_map[1::2], fillvalue="0"):
        disk.extend([file_id for _ in range(int(file_len))])
        disk.extend("." for _ in range(int(free_len)))
        file_id += 1
    return disk


def compact(disk: list[str]) -> None:
    disk_len: int = len(disk)
    while "." in disk:
        file_id = disk.pop()
        if file_id != ".":
            free_id: int = disk.index(".")
            disk[free_id] = file_id

    disk.extend(["." for _ in range(disk_len - len(disk))])
    return


def checksum(disk) -> int:
    result = 0
    for i, file_id in enumerate(disk):
        if file_id == ".":
            break
        result += i * int(file_id)
    return result


def main() -> None:
    input_path: str = os.path.dirname(__file__) + "\\input.txt"
    disk = parse_input(input_path)
    compact(disk)
    print(checksum(disk))


if __name__ == "__main__":
    main()
