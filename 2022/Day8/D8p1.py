# AOC22 D8p1: Treetop Tree House
import os
import numpy as np
from numpy.typing import NDArray
from typing import TypeAlias
from pprint import pprint

t_matrix: TypeAlias = NDArray[np.int_]


def parse_input_file(path: str) -> t_matrix:
    with open(path) as f:
        rows = f.readlines()
        tree_map: t_matrix = np.full((len(rows), len(rows[0].strip())), 0)

        for r, row in enumerate(rows):
            for c, tree_height in enumerate(row.strip()):
                tree_map[r][c] = int(tree_height)
    return tree_map


def main() -> None:
    input_path = os.path.dirname(__file__) + "\\input.txt"
    tree_map: t_matrix = parse_input_file(input_path)
    visible_map: t_matrix = np.full((len(tree_map), len(tree_map[1])), 0)
    # look down
    for c, col in enumerate(tree_map.T):
        visible_map[0][c] = 1
        min_height: int = col[0]
        for t, tree in enumerate(col):
            if tree > min_height:
                visible_map[t][c] = 1
                min_height = tree
        # look up
        col = col[::-1]
        visible_map[-1][c] = 1
        min_height = col[0]
        for t, tree in enumerate(col):
            if tree > min_height:
                visible_map[len(col) - t - 1][c] = 1
                min_height = tree

    # look right
    for r, row in enumerate(tree_map):
        visible_map[r][0] = 1
        min_height = row[0]
        for t, tree in enumerate(row):
            if tree > min_height:
                visible_map[r][t] = 1
                min_height = tree
        # look left
        row = row[::-1]
        visible_map[r][-1] = 1
        min_height = row[0]
        for t, tree in enumerate(row):
            if tree > min_height:
                visible_map[r][len(row) - t - 1] = 1
                min_height = tree
    pprint(visible_map)
    print(np.sum(visible_map == 1))


if __name__ == "__main__":
    main()
