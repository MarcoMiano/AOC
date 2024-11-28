# AOC22 D11p1: Monkey in the Middle
import os
import operator as op

from typing import Callable
from dataclasses import dataclass
from collections import deque
from math import prod

ROUNDS = 20


class Monkey(object):
    def __init__(
        self,
        starting_items: deque[int],
        operator: Callable,
        operand: int,
        condition: int,
        if_true: int,
        if_false: int,
    ):
        self.items = starting_items
        self.operator = operator
        self.operand = operand
        self.condition = condition
        self.if_true = if_true
        self.if_false = if_false
        self._inspected = 0

    def play_turn(self) -> list[tuple[int, int]]:
        throws: list[tuple[int, int]] = list()
        while len(self.items) > 0:
            item = self.items.popleft()
            worry = (
                self.operator(item, self.operand if self.operand >= 0 else item) // 3
            )
            test = worry % self.condition == 0
            throws.append((self.if_true if test else self.if_false, worry))
            self._inspected += 1
        return throws

    def add_item(self, worry: int) -> None:
        self.items.append(worry)

    @property
    def inspections(self) -> int:
        return self._inspected


def parse_input_file(input_path: str) -> list[Monkey]:
    with open(input_path) as f:
        raw_monkeys = f.read().split("\n\n")

    monkeys: list[Monkey] = list()

    for raw_monkey in raw_monkeys:
        raw_monkey = raw_monkey.splitlines()
        starting_items = deque(
            [int(items) for items in raw_monkey[1].split(":")[1].split(", ")]
        )
        raw_operator, raw_operand = raw_monkey[2].split("old ")[1].split(" ")
        match raw_operator:
            case "*":
                operator: Callable = op.mul
            case "+":
                operator: Callable = op.add
            case _:
                raise ValueError("Unknown operator")
        operand = int(raw_operand) if raw_operand != "old" else -1
        condition = int(raw_monkey[3].split("by ")[1])
        if_true = int(raw_monkey[4].split("monkey ")[1])
        if_false = int(raw_monkey[5].split("monkey ")[1])

        monkeys.append(
            Monkey(starting_items, operator, operand, condition, if_true, if_false)
        )
    return monkeys


def main() -> None:
    input_path: str = os.path.dirname(__file__) + "\\input.txt"
    monkeys: list[Monkey] = parse_input_file(input_path)

    for _ in range(ROUNDS):
        for monkey in monkeys:
            throws: list[tuple[int, int]] = monkey.play_turn()
            for m, w in throws:
                monkeys[m].add_item(w)

    inspections: list[int] = list()
    for monkey in monkeys:
        inspections.append(monkey.inspections)

    print(prod(sorted(inspections, reverse=True)[:2]))


if __name__ == "__main__":
    main()
