# AOC23 D15p1: Lens Library


# LPF-HASH -> Lava Production Facility-Holiday ASCII Helper Algorithm
def get_lpf_hash(string: str) -> int:
    output = 0
    for char in string:
        output += ord(char)
        output *= 17
        output %= 256
    return output


def get_checksum(strings: list[str]) -> int:
    output = 0

    for string in strings:
        output += get_lpf_hash(string)

    return output


def main() -> None:
    with open("Day15\\input.txt") as f:
        init_seq: list[str] = f.read().strip("\n").split(",")
    print(get_checksum(init_seq))


if __name__ == "__main__":
    main()
