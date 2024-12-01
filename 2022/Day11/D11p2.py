# AOC22 D11p2: Monkey in the Middle
# Thanks to Luke Skyward https://medium.com/@datasciencedisciple/advent-of-code-2022-in-python-day-11-5832b8f25c21

import os
import operator as op

from typing import Callable
from collections import deque
from math import prod
from pprint import pprint

ROUNDS = 10000


class Item:
    def __init__(self, initial_value: int) -> None:
        self.value = initial_value
        self.divisible_by = {
            i: initial_value % i for i in [2, 3, 5, 7, 11, 13, 17, 19, 23]
        }

    def __repr__(self) -> str:
        return f"Item(value={self.value}, divisible_by={self.divisible_by})"

    def update_item(
        self, operator: Callable[[int, int], int], operand: int = -1
    ) -> None:
        for k in self.divisible_by.keys():
            self.divisible_by[k] = (
                operator(
                    self.divisible_by[k],
                    operand if operand >= 0 else self.divisible_by[k],
                )
                % k
            )


class Monkey(object):
    def __init__(
        self,
        starting_items: deque[Item],
        operator: Callable[[int, int], int],
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

    def __repr__(self) -> str:
        return f"Monkey(items={self.items}"

    def play_turn(self) -> list[tuple[int, Item]]:
        throws: list[tuple[int, Item]] = list()

        for item in self.items:
            item.update_item(self.operator, self.operand)

        while len(self.items) > 0:
            item = self.items.popleft()
            test = item.divisible_by[self.condition] == 0
            throws.append((self.if_true if test else self.if_false, item))
            self._inspected += 1
        return throws

    def add_item(self, item: Item) -> None:
        self.items.append(item)

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
            [Item(int(item)) for item in raw_monkey[1].split(":")[1].split(", ")]
        )
        raw_operator, raw_operand = raw_monkey[2].split("old ")[1].split(" ")
        match raw_operator:
            case "*":
                operator: Callable[[int, int], int] = op.mul
            case "+":
                operator: Callable[[int, int], int] = op.add
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


def print_inspections(monkeys) -> None:
    inspections: list[int] = list()
    for monkey in monkeys:
        inspections.append(monkey.inspections)
    print(prod(sorted(inspections, reverse=True)[:2]))


def main() -> None:
    input_path: str = os.path.dirname(__file__) + "\\input.txt"
    monkeys: list[Monkey] = parse_input_file(input_path)

    for r in range(ROUNDS):
        for monkey in monkeys:
            throws: list[tuple[int, Item]] = monkey.play_turn()
            for m, w in throws:
                monkeys[m].add_item(w)

    print_inspections(monkeys)


if __name__ == "__main__":
    main()
