# AOC22 D1p1: Calorie Counting
def main() -> None:
    elves: list[int] = list()
    with open("2022//Day1//input.txt") as f:
        elf_id = 0
        for line in f.readlines():
            if len(elves) == 0:
                elves.append(0)
            if line.strip() == "":
                elf_id += 1
                elves.append(0)
                continue
            elves[elf_id] += int(line.strip())

    print(max(elves))


if __name__ == "__main__":
    main()
