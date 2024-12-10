# AOC24 D7p2: Brigde Repair
import os

from collections import deque


def parse_input(input_path: str):
    with open(input_path, "r") as f:
        lines = f.readlines()

    result: list[tuple[int, deque[int]]] = list()
    for line in lines:
        test_value, raw_operands = line.split(": ")
        raw_operands = raw_operands.strip().split(" ")
        operands = deque([int(op) for op in raw_operands])
        result.append((int(test_value), operands))

    return result


def int_concat(a: int, b: int) -> int:
    return int(str(a) + str(b))


def test_equation(
    test_value: int, operands: deque[int], op1: int | None = None
) -> bool:
    if op1 is None:
        op1 = operands.popleft()
    op2: int = operands.popleft()
    result = False

    if len(operands) > 0:
        result |= test_equation(test_value, operands.copy(), op1 + op2)
        result |= test_equation(test_value, operands.copy(), op1 * op2)
        result |= test_equation(test_value, operands.copy(), int_concat(op1, op2))
    else:
        result |= test_value == op1 + op2
        result |= test_value == op1 * op2
        result |= test_value == int_concat(op1, op2)

    return result


def main() -> None:
    input_path: str = os.path.dirname(__file__) + "\\input.txt"
    equations = parse_input(input_path)
    result = 0

    for test_value, operands in equations:
        if test_equation(test_value, operands):
            result += test_value

    print(result)


if __name__ == "__main__":
    main()
