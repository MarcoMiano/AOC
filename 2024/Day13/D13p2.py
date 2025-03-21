# AOC24 D13p2: Claw Contraption
import os
from typing import TypeAlias
from sympy import symbols, Eq, solve

T_machine: TypeAlias = tuple[int, int, int, int, int, int]
T_machines: TypeAlias = list[T_machine]

OFFSET = 10_000_000_000_000


def parse_input(input_path: str) -> T_machines:
    machines = list()
    with open(input_path, "r") as file:
        raw_machines: list[str] = file.read().split("\n\n")
    for raw_machine in raw_machines:
        btn_A, btn_B, prize = raw_machine.split("\n")
        btn_Ax, btn_Ay = map(int, btn_A.split(": X+")[1].split(", Y+"))
        btn_Bx, btn_By = map(int, btn_B.split(": X+")[1].split(", Y+"))
        prize_x, prize_y = map(int, prize.split(": X=")[1].split(", Y="))
        machines.append(
            (btn_Ax, btn_Ay, btn_Bx, btn_By, prize_x + OFFSET, prize_y + OFFSET)
        )
    return machines


def min_token(machine: T_machine) -> int | None:
    a, b = symbols("a b", integer=True, nonnegative=True)

    solutions = solve(
        (
            Eq(a * machine[0] + b * machine[2], machine[4]),
            Eq(a * machine[1] + b * machine[3], machine[5]),
        ),
        (a, b),
        dict=True,
    )
    valid_solutions = [sol for sol in solutions if sol[a] >= 0 and sol[b] >= 0]

    if not valid_solutions:
        return None

    min_solution = min(valid_solutions, key=lambda sol: sol[a] + sol[b])

    return min_solution[a] * 3 + min_solution[b]


def main() -> None:
    result = 0
    input_path: str = os.path.dirname(__file__) + "\\input-sm.txt"
    machines: T_machines = parse_input(input_path)
    for machine in machines:
        if (tokens := min_token(machine)) is not None:
            result += tokens
    print(result)


if __name__ == "__main__":
    main()
