# AOC23 D2p1: Cube Cunundrum
import re
from io import TextIOWrapper

RED_CUBES = 12
GREEN_CUBES = 13
BLU_CUBES = 14


def parse_game_file(input_file: TextIOWrapper) -> dict[int, dict[int, dict[str, int]]]:
    """
    Parse a Day2 input file of AoC2023 into a dict.

    Parameters:
    - input_file: TextIOWrapper object obtained from a open() containing the input file to parse

    Returns:
    - dict: return a dict with the whole input file parsed in a "JSON" style

    Return example:
    ```python
    {1: {
        0: {'blue': 2, 'red': 3},
        1: {'blue': 3, 'green': 3, 'red': 6},
        2: {'blue': 4, 'red': 6},
        3: {'blue': 2, 'green': 2, 'red': 9},
        4: {'blue': 4, 'red': 2}
        },
    2: {
        0: {'green': 1, 'red': 4},
        1: {'red': 3},
        2: {'blue': 3, 'green': 13, 'red': 5},
        3: {'green': 3, 'red': 2},
        4: {'blue': 3, 'green': 3, 'red': 5},
        5: {'blue': 3, 'green': 12, 'red': 2}
        },
    }
    ```
    """
    output = {}
    for line in input_file:
        line = line.strip("\n")

        game_id = int(re.search(r"\d+", line).group())
        output[game_id] = {}

        game_sets = line[(line.find(":") + 2) :].split(";")

        game_set_id = 0
        for game_set in game_sets:
            output[game_id][game_set_id] = {}
            group_cubes = game_set.split(",")
            for cubes in group_cubes:
                number_of_cubes, color = cubes.strip().split(" ")
                output[game_id][game_set_id][color] = int(number_of_cubes)
            game_set_id += 1
        game_id += 1
    return output


def check_game(games: dict, game_id: int) -> int:
    for game_set_id in games[game_id]:
        for color, number_of_cubes in games[game_id][game_set_id].items():
            match color:
                case "blue":
                    if number_of_cubes > BLU_CUBES:
                        return 0
                case "green":
                    if number_of_cubes > GREEN_CUBES:
                        return 0
                case "red":
                    if number_of_cubes > RED_CUBES:
                        return 0
    return game_id


def main() -> None:
    games = {}

    with open("input.txt", "r") as lines:
        games = parse_game_file(lines)
    answer = 0

    for game_id in games:
        result = check_game(games, game_id)
        answer += result

    print(answer)


if __name__ == "__main__":
    main()
