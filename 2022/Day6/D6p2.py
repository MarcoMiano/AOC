# AOC22 D6p2: Tuning Trouble

import os
from collections import deque, Counter
from pprint import pprint


def main() -> None:
    input_path = os.path.dirname(__file__) + "\\input.txt"
    signal = list()
    with open(input_path) as f:
        signal = list(f.read().strip())
    buffer_sopm = deque(4 * [""], 4)
    buffer_somm = deque(14 * [""], 14)
    sopm = False
    somm = 0
    for c, char in enumerate(signal):
        if sopm == False:
            if len(Counter(buffer_sopm)) == 4 and not "" in buffer_sopm:
                sopm = True
            else:
                buffer_sopm.appendleft(char)
                buffer_somm.appendleft(char)
        else:
            if len(Counter(buffer_somm)) == 14 and not "" in buffer_somm:
                somm = c
                break
            else:
                buffer_somm.appendleft(char)

    print(somm)


if __name__ == "__main__":
    main()
