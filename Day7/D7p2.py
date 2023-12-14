# AOC23 D7p1: Camel Cards
from collections import defaultdict
from email.policy import default
from functools import cmp_to_key

LABELS = "AKQT98765432J"


def get_type(hand: str) -> int:
    counts = defaultdict(int)

    for card in hand:
        counts[card] += 1

    if hand.find("J") > -1 and counts["J"] != 5:
        jokers = counts.pop("J")
        counts[max(counts, key=counts.get)] += jokers

    sorted_counts = sorted(counts.values())

    if sorted_counts == [5]:
        return 7
    if sorted_counts == [1, 4]:
        return 6
    if sorted_counts == [2, 3]:
        return 5
    if sorted_counts == [1, 1, 3]:
        return 4
    if sorted_counts == [1, 2, 2]:
        return 3
    if sorted_counts == [1, 1, 1, 2]:
        return 2
    else:
        return 1


def compare(x: str, y: str) -> int:
    x_type = get_type(x)
    y_type = get_type(y)
    if x_type == y_type:
        if x == y:
            return 0
        for char_x, char_y in zip(x, y):
            if LABELS.index(char_x) < LABELS.index(char_y):
                return 1
            if LABELS.index(char_x) > LABELS.index(char_y):
                return -1
    elif x_type > y_type:
        return 1
    return -1


def main() -> None:
    with open("Day7\\input.txt") as f:
        input_file = f.read().strip().split("\n")

    unranked_hands = []
    for hand_bid in input_file:
        hand_bid = hand_bid.split()
        unranked_hands.append([hand_bid[0], int(hand_bid[1])])

    ranked_hands = sorted(
        unranked_hands, key=cmp_to_key(lambda x, y: compare(x[0], y[0]))
    )

    answer = 0
    for i, hand in enumerate(ranked_hands):
        answer += (i + 1) * hand[1]
    print(answer)


if __name__ == "__main__":
    main()
