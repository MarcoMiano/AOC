# AOC23 D8p1: Haunted Wasteland
from collections import defaultdict
import math
import re


class Navigator(object):
    def __init__(
        self, instructions: str, nodes: defaultdict, starting_node: str
    ) -> None:
        self.instructions = instructions
        self.nodes = nodes
        self.current_node: str = starting_node
        self.i = 0

    def next_node(self) -> str:
        self.current_node = self.nodes[self.current_node][
            int(self.instructions[self.i])
        ]

        self.i = (self.i + 1) if self.i + 1 < self.instructions.__len__() else 0
        return self.current_node


def parse_input_file(input_file: list) -> defaultdict:
    output = defaultdict()

    for node in input_file:
        node = re.sub(r"[=(),]", " ", node).strip()
        node = re.sub(r"\s{2,}", " ", node).split()

        output[node[0]] = [node[1], node[2]]

    return output


def navigate(navigators: list[Navigator]) -> list[int]:
    output = []

    i = 1

    while navigators:
        current_nodes = []
        to_pop = []
        for navigator_index, navigator in enumerate(navigators):
            node = navigator.next_node()
            if node.endswith("Z"):
                output.append(i)
                to_pop.append(navigator_index)

        for z in to_pop:
            navigators.pop(z)

        i += 1

    return output


def main() -> None:
    with open("Day8\\input.txt") as f:
        input_file = f.read().strip().split("\n")

    instructions = input_file.pop(0).strip()
    input_file.pop(0)

    instructions = re.sub(r"L", "0", instructions)
    instructions = re.sub(r"R", "1", instructions)

    nodes = parse_input_file(input_file)

    navigators: list(Navigator) = []

    for node in nodes:
        if node.endswith("A"):
            navigators.append(Navigator(instructions, nodes, node))

    steps = navigate(navigators)

    print(steps)

    answer = math.lcm(*steps)

    print(answer)


if __name__ == "__main__":
    main()
