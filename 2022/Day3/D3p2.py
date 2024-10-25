# AOC22 D3p2: Rucksack Reorganization

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
        elves_group: list[Counter] = list()
        for l, line in enumerate(f.readlines()):
            elves_group.append(Counter(line.strip()))
            if len(elves_group) == 3:
                badge_item: str = list(
                    (elves_group[0] & elves_group[1] & elves_group[2]).keys()
                )[0]
                priority += item_priority(badge_item)
                elves_group.clear()

    print(priority)


if __name__ == "__main__":
    main()
