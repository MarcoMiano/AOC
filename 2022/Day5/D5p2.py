# AOC22 D5p2: Supply Stacks

import os
from pprint import pprint
from collections import deque
from typing import TypeAlias

t_stacks: TypeAlias = list[list[str]]
t_instructions: TypeAlias = list[dict[str, int]]


def parse_input_file(path: str) -> tuple[t_stacks, t_instructions]:
    with open(path) as f:
        rows: t_stacks = list()
        instructions: t_instructions = list()
        b_instruction = False
        for line in f.readlines():
            if line == "\n":
                b_instruction = True
                continue
            if b_instruction:
                line = line.split()
                instruction = {
                    "move": int(line[1]),
                    "from": int(line[3]) - 1,
                    "to": int(line[5]) - 1,
                }
                instructions.append(instruction)
            else:
                line = [
                    line.strip("\n")[i : i + 4].strip("[] ")
                    for i in range(0, len(line), 4)
                ]
                if line[0] == "1":
                    continue
                rows.append(line)
        stacks: t_stacks = [list(reversed(col)) for col in zip(*rows)]
        stacks = [[element for element in row if element] for row in stacks]
    return (stacks, instructions)


def main() -> None:
    input_path = os.path.dirname(__file__) + "\\input.txt"
    stacks, instructions = parse_input_file(input_path)
    for instr in instructions:
        if instr["move"] == 1:
            stacks[instr["to"]].append(stacks[instr["from"]].pop())
        else:
            stacks[instr["to"]].extend(stacks[instr["from"]][-instr["move"] :])
            stacks[instr["from"]] = stacks[instr["from"]][: -instr["move"]]
    answer = str()
    for stack in stacks:
        if len(stack) == 0:
            continue
        answer += stack[-1]
    print(answer)


if __name__ == "__main__":
    main()
