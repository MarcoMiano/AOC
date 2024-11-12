# AOC22 D8p2: Treetop Tree House
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


def calculate_scenic_score(trees, cur_tree) -> int:
    score = 0
    for tree in trees:
        if tree < cur_tree:
            score += 1
        else:
            score += 1
            break
    return score


def main() -> None:
    input_path = os.path.dirname(__file__) + "\\input.txt"
    tree_map: t_matrix = parse_input_file(input_path)
    score_map: t_matrix = np.full((len(tree_map), len(tree_map[1])), 1)
    for r, row in enumerate(tree_map):
        for t, tree in enumerate(row):
            # look down
            down_trees = tree_map.T[t][r + 1 :]
            score_map[r][t] *= calculate_scenic_score(down_trees, tree)
            # look up
            up_trees = tree_map.T[t][:r][::-1]
            score_map[r][t] *= calculate_scenic_score(up_trees, tree)
            # look right
            right_trees = tree_map[r][t + 1 :]
            score_map[r][t] *= calculate_scenic_score(right_trees, tree)
            # look left
            left_trees = tree_map[r][:t][::-1]
            score_map[r][t] *= calculate_scenic_score(left_trees, tree)

    print(score_map.max())


if __name__ == "__main__":
    main()
