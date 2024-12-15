# AOC24 D9p2: Disk Fragmenter
import os

from itertools import zip_longest


def parse_input(input_path: str) -> list[tuple[int, int]]:
    with open(input_path, "r") as f:
        disk_map: str = f.read()

    # (file_id, block_len) file_id -> -1 = free_space
    disk: list[tuple[int, int]] = list()
    file_id = 0

    for file_len, free_len in zip_longest(disk_map[::2], disk_map[1::2], fillvalue="0"):
        file_len = int(file_len)
        free_len = int(free_len)
        disk.append((file_id, file_len))
        if free_len > 0:
            disk.append((-1, free_len))
        file_id += 1

    return disk


def print_disk(disk: list[tuple[int, int]]) -> None:
    for block_id, block_len in disk:
        for _ in range(block_len):
            print(block_id if block_id != -1 else ".", end="")
    print()


def compact(disk: list[tuple[int, int]]) -> None:
    def next_file(file_id) -> int:
        i: int = len(disk) - 1
        while i >= 0:
            if disk[i][0] == -1:
                i -= 1
                continue
            if disk[i][0] < file_id:
                break
            i -= 1
        else:
            i = -1
        return i

    def first_free(free_len: int) -> int:
        j = 0
        while j < len(disk):
            if disk[j][0] != -1:
                j += 1
                continue
            if disk[j][1] >= free_len:
                break
            j += 1
        else:
            j = -1
        return j

    i = next_file(100000)
    j = 0

    while i >= 0:
        file_id, file_len = disk[i]
        print(f"i: {i}, file_id: {file_id}")
        if j == len(disk):
            j = 0
            i = next_file(file_id)
            continue

        j = first_free(file_len)
        print(f"j: {j}")
        if j == -1:
            i = next_file(file_id)
            continue
        if j > i:
            j = 0
            i = next_file(file_id)
            continue

        free_len: int = disk[j][1]

        if free_len == file_len:
            disk[j] = (file_id, file_len)
            disk[i] = (-1, file_len)
        elif free_len > file_len:
            disk[j] = (-1, free_len - file_len)
            disk[i] = (-1, file_len)
            disk.insert(j, (file_id, file_len))

        i = next_file(file_id)
    return


def checksum(disk: list[tuple[int, int]]) -> int:
    result = 0
    i = 0
    for block_id, block_len in disk:
        if block_id == -1:
            i += block_len
            continue
        for _ in range(block_len):
            result += i * block_id
            i += 1
    return result


def main() -> None:
    input_path: str = os.path.dirname(__file__) + "\\input.txt"
    disk: list[tuple[int, int]] = parse_input(input_path)
    compact(disk)
    print_disk(disk)
    print(checksum(disk))


if __name__ == "__main__":
    main()
