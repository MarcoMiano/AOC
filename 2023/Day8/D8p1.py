# AOC23 D8p1: Haunted Wasteland
from collections import defaultdict
import re


def parse_input_file(input_file: list) -> defaultdict:
    output = defaultdict()

    for node in input_file:
        node = re.sub(r"[=(),]", " ", node).strip()
        node = re.sub(r"\s{2,}", " ", node).split()

        output[node[0]] = [node[1], node[2]]

    return output


def navigate(instructions: str, nodes: defaultdict) -> int:
    output = 0

    instructions = re.sub(r"L", "0", instructions)
    instructions = re.sub(r"R", "1", instructions)

    current_node = "AAA"
    i = 0
    while current_node != "ZZZ":
        current_node = nodes[current_node][int(instructions[i])]

        output += 1
        i = (i + 1) if i + 1 < instructions.__len__() else 0

    return output


def main() -> None:
    with open("2023//Day8//input.txt") as f:
        input_file = f.read().strip().split("\n")

    instructions = input_file.pop(0).strip()
    input_file.pop(0)

    nodes = parse_input_file(input_file)
    ans = navigate(instructions, nodes)

    print(ans)


if __name__ == "__main__":
    main()
