# AOC22 D6p1: Tuning Trouble

import os
from collections import deque, Counter
from pprint import pprint


def main() -> None:
    input_path = os.path.dirname(__file__) + "\\input.txt"
    signal = list()
    with open(input_path) as f:
        signal = list(f.read().strip())
    buffer = deque(["", "", "", ""], 4)
    sopm = 0
    for c, char in enumerate(signal):
        if len(Counter(buffer)) == 4 and not "" in buffer:
            sopm: int = c
            break
        buffer.appendleft(char)
    print(sopm)


if __name__ == "__main__":
    main()
