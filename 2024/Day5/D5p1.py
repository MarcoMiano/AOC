# AOC24 D5p1: Print Queue
import os


def parse_input(input_path) -> tuple[dict[str, list[str]], list[list[str]]]:
    rules: dict[str, list[str]] = dict()
    with open(input_path) as f:
        raw_rules, raw_pages = f.read().split("\n\n")

    for rule in raw_rules.splitlines():
        r1, r2 = rule.split("|")
        if r1 not in rules.keys():
            rules[r1] = [r2]
        else:
            rules[r1].append(r2)

    updates: list[list[str]] = [
        [page for page in update.split(",")] for update in raw_pages.splitlines()
    ]

    return rules, updates


def main() -> None:
    input_path: str = os.path.dirname(__file__) + "\\input.txt"
    rules, updates = parse_input(input_path)

    result = 0
    for update in updates:
        for i in range(len(update) - 1, 0, -1):
            page = update[i]
            if page not in rules.keys():
                continue
            br: bool = False
            for u in update[:i]:
                if u in rules[page]:
                    br = not br
                    break
            if br:
                break
        else:
            result += int(update[len(update) // 2])

    print(result)


if __name__ == "__main__":
    main()
