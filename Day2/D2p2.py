# AOC23 D2p1: Cube Cunundrum
from D2p1 import parse_game_file

# games = {
#   1: {0: {'blue': 2, 'red': 3},
#       1: {'blue': 3, 'green': 3, 'red': 6},
#       2: {'blue': 4, 'red': 6},
#       3: {'blue': 2, 'green': 2, 'red': 9},
#       4: {'blue': 4, 'red': 2}},
#   2: {0: {'green': 1, 'red': 4},
#       1: {'red': 3},
#       2: {'blue': 3, 'green': 13, 'red': 5},
#       3: {'green': 3, 'red': 2},
#       4: {'blue': 3, 'green': 3, 'red': 5},
#       5: {'blue': 3, 'green': 12, 'red': 2}},
# }
COLORS = ["blue", "green", "red"]


def check_game(games: dict, game_id: int) -> int:
    minimum_required_cubes = {"blue": 1, "green": 1, "red": 1}

    for game_set_id in games[game_id]:
        for color in COLORS:
            try:
                if games[game_id][game_set_id][color] > minimum_required_cubes[color]:
                    minimum_required_cubes[color] = games[game_id][game_set_id][color]
            except:
                pass

    power = 1
    for num in minimum_required_cubes.values():
        power *= num
    return power


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
