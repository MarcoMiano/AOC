# AOC24 D17p2: Chronospatial Computer
import os
from enum import IntEnum
from collections import deque


class OPCODE(IntEnum):
    ADV = 0
    BXL = 1
    BST = 2
    JNZ = 3
    BXC = 4
    OUT = 5
    BDV = 6
    CDV = 7


class Cpu(object):
    def __init__(self, reg_a: int, reg_b: int, reg_c: int, program: list[int]) -> None:
        self.reg_a: int = reg_a
        self.reg_b: int = reg_b
        self.reg_c: int = reg_c
        self.reg_a0 = 0
        self.reg_b0 = 0
        self.reg_c0 = 0
        self.rom: list[int] = program
        self.pc: int = 0
        self.output: list[int] = [0 for _ in range(len(self.rom))]
        self.out_cursor = 0

    def _fetch(self):
        opcode, operand = self.rom[self.pc], self.rom[self.pc + 1]
        self.pc += 2
        return opcode, operand

    def _combo(self, operand: int) -> int:
        match operand:
            case 0 | 1 | 2 | 3 as o:
                return o
            case 4:
                return self.reg_a
            case 5:
                return self.reg_b
            case 6:
                return self.reg_c
            case 7:
                raise ValueError("Invalid combo operand: 7 is reserved")
            case _:
                raise ValueError(f"Invalid combo operand: {operand}.")

    def _out(self, o: int) -> None:
        self.output[self.out_cursor] = o
        self.out_cursor += 1

    def execute(self) -> None:
        self.output = [0 for _ in range(len(self.rom))]
        self.pc = 0
        self.out_cursor = 0
        while self.pc < len(self.rom):
            opcode, operand = self._fetch()
            match opcode:
                case OPCODE.ADV:
                    # 0 Division: REG.A = REG.A // (2 ** c_operand)
                    self.reg_a //= 2 ** self._combo(operand)
                case OPCODE.BXL:
                    # 1 Bitwise XOR: REG.B = REG.B ^ operand
                    self.reg_b ^= operand
                case OPCODE.BST:
                    # 2 Modulo 8: REG.B = c_operand%8
                    self.reg_b = self._combo(operand) % 8
                case OPCODE.JNZ:
                    # 3 Jump non zero: if REG.A is not 0 -> pc = operator
                    self.pc = operand if self.reg_a != 0 else self.pc
                case OPCODE.BXC:
                    # 4 Bitwise XOR: REG.B = REG.B ^ REG.C
                    self.reg_b ^= self.reg_c
                case OPCODE.OUT:
                    # 5 Output: OUT.append(c_operand % 8)
                    self._out(self._combo(operand) % 8)
                case OPCODE.BDV:
                    # 6 Division: REG.B = REG.A // (2 ** c_operand)
                    self.reg_b = self.reg_a // (2 ** self._combo(operand))
                case OPCODE.CDV:
                    # 7 Division: REG.C = REG.A // (2 ** c_operand)
                    self.reg_c = self.reg_a // (2 ** self._combo(operand))
                case _:
                    raise ValueError(f"Invalid opcode: {opcode}")


def parse_input(input_path: str):
    text = open(input_path).read().splitlines()
    assert len(text) == 5
    reg_a = int(text[0].split("A: ")[1])
    reg_b = int(text[1].split("B: ")[1])
    reg_c = int(text[2].split("C: ")[1])
    program: list[int] = [int(s) for s in text[4].split("Program: ")[1].split(",")]
    return Cpu(reg_a, reg_b, reg_c, program)


def bin48_tribits(n: int, other_string: str = "", length: int = 48) -> str:
    fmt = "0" + str(length) + "b"
    bits = format(n, fmt)
    groups = [bits[i : i + 3] for i in range(0, length, 3)]
    return "0b " + " ".join(groups) + other_string


def list_to_octal(input_list: list[int]) -> int:
    result = 0
    for t, tribit in enumerate(input_list[::-1]):
        result += tribit << (t * 3)
    return result


def main() -> None:
    input_path: str = os.path.dirname(__file__) + "\\input.txt"
    cpu: Cpu = parse_input(input_path)
    queue: deque[tuple[list[int], int]] = deque()
    queue.append(
        ([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 15)
    )  # start with empty state to find bit 15.
    reg_try: list[int] = list()
    solutions: list[int] = list()
    while queue:
        reg_try, tribit = queue.pop()
        for test in range(0, 8):
            reg_try[15 - tribit] = test
            cpu.reg_a = list_to_octal(reg_try)
            cpu.execute()
            if cpu.output == cpu.rom:
                solutions.append(list_to_octal(reg_try))
                continue
            if cpu.output[tribit:] == cpu.rom[tribit:]:
                queue.append((reg_try.copy(), tribit - 1))
    if solutions:
        print(min(solutions))
    else:
        print("Solution NOT Found")


if __name__ == "__main__":
    main()
