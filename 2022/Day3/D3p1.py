# AOC22 D3p1: Rucksack Reorganization

from _collections_abc import dict_keys
from collections import Counter
from typing import TypeAlias

t_rucksacks: TypeAlias = list[tuple[Counter, Counter]]


def item_priority(item: str) -> int:
    return ord(item) - (96 if item.islower() else 38)


def main() -> None:
    rucksacks: t_rucksacks = list()
    priority: int = 0
    with open("2022//Day3//input.txt") as f:
        for line in f.readlines():
            half_len = len(line) // 2
            comp1 = Counter(line.strip()[:half_len])
            comp2 = Counter(line.strip()[half_len:])
            common_items: dict_keys[str, int] = (comp1 & comp2).keys()
            priority += sum([item_priority(item) for item in common_items])
    print(priority)


if __name__ == "__main__":
    main()
