# AOC23 D4p1: Scratchcards


def main() -> None:
    with open("2023//Day4//input.txt") as f:
        input_file = f.read().strip().split("\n")

    points = 0

    for line in input_file:
        count = 0
        _, numbers = line.split(":")
        winning_numbers, my_numbers = numbers.split("|")
        winning_numbers = winning_numbers.strip().replace("  ", " ").split(" ")
        my_numbers = my_numbers.strip().replace("  ", " ").split(" ")
        for number in my_numbers:
            if number in winning_numbers:
                count += 1
        match count:
            case 0:
                points += 0
            case 1:
                points += 1
            case _:
                points += 2 ** (count - 1)

    print(points)


if __name__ == "__main__":
    main()
