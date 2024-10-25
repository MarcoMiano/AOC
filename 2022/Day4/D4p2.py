# AOC22 D4p2: Camp Cleanup


def main() -> None:
    overlapped = 0
    with open("2022//Day4//input.txt") as f:
        for line in f.readlines():
            pair1, pair2 = [
                tuple(map(int, pair.split("-"))) for pair in line.strip().split(",")
            ]
            if (
                pair1[0] <= pair2[0] <= pair1[1]
                or pair1[0] <= pair2[1] <= pair1[1]
                or pair2[0] <= pair1[0] <= pair2[1]
                or pair2[0] <= pair1[1] <= pair2[1]
            ):
                overlapped += 1
        print(overlapped)


if __name__ == "__main__":
    main()
