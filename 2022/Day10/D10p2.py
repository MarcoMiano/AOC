# AOC22 D10p2: Cathode-Ray Tube
import os
from dataclasses import dataclass
from typing import TypeAlias
from enum import Enum


#### OPCODES ####
class OpCode(Enum):
    noop = 0
    addx = 1


@dataclass
class Instruction(object):
    opcode: OpCode
    operand: int | None = None


t_program: TypeAlias = list[Instruction]
t_screen: TypeAlias = list[list[str]]


class CPU(object):
    def __init__(self) -> None:
        self.reg_x = 1
        self.pc = 0
        self.screen: t_screen = [["."] * 40 for _ in range(6)]

    def update_screen(self) -> None:
        x: int = self.pc % 40
        y: int = (self.pc // 40) % 6
        sprite_present: bool = abs(x - self.reg_x) <= 1

        self.screen[y][x] = "#" if sprite_present else "."

    def increment_pc(self, cycles: int) -> None:
        while cycles > 0:
            self.update_screen()
            self.pc += 1
            cycles -= 1

    def run(self, program: t_program) -> None:
        for instruction in program:
            match instruction.opcode:
                case OpCode.noop:
                    self.increment_pc(1)
                case OpCode.addx:
                    if instruction.operand is None:
                        raise TypeError("ERROR: Operand of OP_ADDX cannot be None")
                    self.increment_pc(2)
                    self.reg_x += instruction.operand
                case _:
                    raise ValueError("ERROR: UNKOWN opcode")

    def print_screen(self) -> None:
        for line in self.screen:
            print("".join(line))


def parse_input_file(input_path: str) -> t_program:
    program: t_program = list()
    with open(input_path) as f:
        for raw_inst in f.readlines():
            raw_inst = raw_inst.strip().split()

            opcode: OpCode = OpCode[raw_inst[0]]
            operand: int | None = int(raw_inst[1]) if len(raw_inst) == 2 else None

            program.append(Instruction(opcode, operand))
    return program


def main() -> None:
    input_path = os.path.dirname(__file__) + "\\input.txt"
    program: t_program = parse_input_file(input_path)

    cpu = CPU()
    cpu.run(program)
    cpu.print_screen()


if __name__ == "__main__":
    main()
