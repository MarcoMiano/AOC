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
        self.rom: list[int] = program
        self.pc: int = 0
        self.output: list[int] = []

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

    def execute(self) -> None:
        self.pc = 0
        self.output: list[int] = []
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
                    self.output.append(self._combo(operand) % 8)
                case OPCODE.BDV:
                    # 6 Division: REG.B = REG.A // (2 ** c_operand)
                    self.reg_b = self.reg_a // (2 ** self._combo(operand))
                case OPCODE.CDV:
                    # 7 Division: REG.C = REG.A // (2 ** c_operand)
                    self.reg_c = self.reg_a // (2 ** self._combo(operand))
                case _:
                    raise ValueError(f"Invalid opcode: {opcode}")

    @property
    def out(self) -> str:
        if not self.output:
            return ""
        result: str = ""
        for element in self.output:
            result += str(element) + ","
        return result[:-1]


def parse_input(input_path: str):
    text = open(input_path).read().splitlines()
    assert len(text) == 5
    reg_a = int(text[0].split("A: ")[1])
    reg_b = int(text[1].split("B: ")[1])
    reg_c = int(text[2].split("C: ")[1])
    program: list[int] = [int(s) for s in text[4].split("Program: ")[1].split(",")]
    return Cpu(reg_a, reg_b, reg_c, program)


def main() -> None:
    input_path: str = os.path.dirname(__file__) + "\\input.txt"
    cpu: Cpu = parse_input(input_path)
    i = 0o0000_0000_0000_0000
    poss = deque()
    const = 0o1000_0000_0000_0000
    digit = 16
    for l in range(8):
        i = l * const >> (3 * (17 - digit))
        cpu.reg_a = i
        cpu.execute()
        if cpu.output[digit - 17] == cpu.rom[digit - 1]:
            poss.append((i, digit))
            print(poss)
    while poss:
        i_old, digit = poss.pop()
        print(f"0o{i_old:016o}")
        digit -= 1
        for l in range(8):
            i = i_old + l * const << (3 * (17 - digit))
            print(f"0o{i:016o}")
            cpu.reg_a = i
            cpu.execute()
            print(cpu.out)
            if cpu.output[digit - 17] == cpu.rom[digit - 1]:
                poss.append((i, digit))
                print(poss)


if __name__ == "__main__":
    main()
