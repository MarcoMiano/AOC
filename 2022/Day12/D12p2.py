# AOC22 D11p1: Monkey in the Middle
import os
import numpy as np

from typing import TypeAlias
from pprint import pprint
from itertools import product

t_coord: TypeAlias = tuple[int, int]
t_distances: TypeAlias = dict[t_coord, float | int]

S: int = ord("S") - 97
E: int = ord("E") - 97


def iter_dijkstra(
    height_map: np.ndarray,
    cur_coord: t_coord,
    distances: t_distances,
    visited_coord: list[t_coord],
) -> tuple[t_distances, list[t_coord]]:

    def check_step(next_coord: t_coord) -> bool:
        if (
            height_map[next_coord[0]][next_coord[1]] + 1
            >= height_map[cur_coord[0]][cur_coord[1]]
        ):
            return True
        else:
            return False

    def update_distance(next_coord: t_coord) -> t_distances:
        if distances[next_coord] == np.inf:
            distances[next_coord] = distances[cur_coord] + 1
            return distances
        elif distances[next_coord] > distances[cur_coord] + 1:
            return distances
        else:
            return distances

    next_coord_down: t_coord = (cur_coord[0] + 1, cur_coord[1])
    next_coord_up: t_coord = (cur_coord[0] - 1, cur_coord[1])
    next_coord_right: t_coord = (cur_coord[0], cur_coord[1] + 1)
    next_coord_left: t_coord = (cur_coord[0], cur_coord[1] - 1)

    if (
        (cur_coord[0] < height_map.shape[0] - 1)
        and (check_step(next_coord_down))
        and next_coord_down not in visited_coord
    ):
        distances = update_distance(next_coord_down)

    if (
        (cur_coord[0] > 0)
        and (check_step(next_coord_up))
        and next_coord_up not in visited_coord
    ):
        distances = update_distance(next_coord_up)

    if (
        (cur_coord[1] < height_map.shape[1] - 1)
        and (check_step(next_coord_right))
        and next_coord_right not in visited_coord
    ):
        distances = update_distance(next_coord_right)

    if (
        (cur_coord[1] > 0)
        and (check_step(next_coord_left))
        and next_coord_left not in visited_coord
    ):
        distances = update_distance(next_coord_left)

    visited_coord.append(cur_coord)

    return distances, visited_coord


def main() -> None:
    input_path: str = os.path.dirname(__file__) + "\\input.txt"
    with open(input_path) as f:
        input_list = f.readlines()
    height_map: np.ndarray = np.array(
        [[ord(letter) - 97 for letter in line.strip()] for line in input_list]
    )

    s_coord: t_coord = np.where(height_map == S)[0][0], np.where(height_map == S)[1][0]
    e_coord: t_coord = np.where(height_map == E)[0][0], np.where(height_map == E)[1][0]

    distances: t_distances = {
        key: np.inf
        for key in list(product(range(height_map.shape[0]), range(height_map.shape[1])))
    }

    distances[e_coord] = 0

    height_map[s_coord[0], s_coord[1]] = ord("a") - 97
    height_map[e_coord[0], e_coord[1]] = ord("z") - 97

    visited_coord: list[t_coord] = list()
    cur_coord: t_coord = e_coord
    univisited_coord: list[t_coord] = list(distances.keys())
    a_coords: list[t_coord] = list(
        zip(np.where(height_map == 0)[0], np.where(height_map == 0)[1])
    )

    while a_coords not in visited_coord:
        distances, visited_coord = iter_dijkstra(
            height_map, cur_coord, distances, visited_coord
        )
        univisited_coord.remove(cur_coord)

        univisited_dict: t_distances = {
            key: distance
            for key, distance in distances.items()
            if key in univisited_coord
        }
        if univisited_dict:
            cur_coord: tuple[int, int] = min(univisited_dict, key=univisited_dict.get)
        else:
            break
        print(cur_coord)

    print(min([value for key, value in distances.items() if key in a_coords]))


if __name__ == "__main__":
    main()
