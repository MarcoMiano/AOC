# AOC22 D1p2: Rock Paper Scissor

# A: Rock 1, B: Paper 2, C: Scissors 3
# X: Lose 0, Y: Draw 3, Z: Win 6

OUTCOMES: dict[tuple[str, str], int] = {
    ("A", "X"): 3,
    ("A", "Y"): 4,
    ("A", "Z"): 8,
    ("B", "X"): 1,
    ("B", "Y"): 5,
    ("B", "Z"): 9,
    ("C", "X"): 2,
    ("C", "Y"): 6,
    ("C", "Z"): 7,
}


def main() -> None:
    score = 0
    with open("2022//Day2//input.txt") as f:
        for line in f.readlines():
            pair: tuple[str, str] = tuple(line.strip().split(maxsplit=1))
            score += OUTCOMES[pair]
    print(score)


if __name__ == "__main__":
    main()
