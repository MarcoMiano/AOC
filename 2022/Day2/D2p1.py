# AOC22 D1p1: Rock Paper Scissor

# A: Rock, B: Paper, C: Scissors
# X: Rock, Y: Paper, Z: Scissors

OUTCOMES: dict[tuple[str, str], int] = {
    ("A", "X"): 4,
    ("A", "Y"): 8,
    ("A", "Z"): 3,
    ("B", "X"): 1,
    ("B", "Y"): 5,
    ("B", "Z"): 9,
    ("C", "X"): 7,
    ("C", "Y"): 2,
    ("C", "Z"): 6,
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
