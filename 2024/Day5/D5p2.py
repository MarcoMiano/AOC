# AOC24 D5p2: Print Queue
import os


def parse_input(input_path) -> tuple[dict[str, set[str]], list[list[str]]]:
    rules: dict[str, set[str]] = dict()
    with open(input_path) as f:
        raw_rules, raw_pages = f.read().split("\n\n")

    for rule in raw_rules.splitlines():
        r1, r2 = rule.split("|")
        if r1 not in rules.keys():
            rules[r1] = {r2}
        else:
            rules[r1].add(r2)

    updates: list[list[str]] = [
        [page for page in update.split(",")] for update in raw_pages.splitlines()
    ]

    return rules, updates


def main() -> None:
    input_path: str = os.path.dirname(__file__) + "\\input.txt"
    rules, updates = parse_input(input_path)

    result = 0
    incorrect_updates: list[list[str]] = list()
    for update in updates:
        for j in range(len(update) - 1, 0, -1):
            page = update[j]
            if page not in rules.keys():
                continue
            br: bool = False
            for p in update[:j]:
                if p in rules[page]:
                    br = True
                    break
            if br:
                incorrect_updates.append(update)
                break
    i = 0
    while i != len(incorrect_updates):
        update = incorrect_updates[i]
        j = len(update) - 1
        while j != 0:
            page = update[j]
            if page in rules.keys():
                errors = set(update[:j]) & rules[page]
                if errors:
                    for error in errors:
                        e = update.index(error)
                        update[j], update[e] = update[e], update[j]
                        break
                    continue
            j -= 1
        result += int(update[len(update) // 2])
        i += 1

    print(result)


if __name__ == "__main__":
    main()
