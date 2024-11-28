# AOC22 D10p1: Cathode-Ray Tube
import os
from dataclasses import dataclass
from typing import TypeAlias
from enum import Enum


#### OPCODES ####
class OpCode(Enum):
    noop = 0
    addx = 1


#################

SIGNAL_STRENGTH_CHECKS = [20, 60, 100, 140, 180, 220]


@dataclass
class Instruction(object):
    opcode: OpCode
    operand: int | None = None


t_program: TypeAlias = list[Instruction]


class CPU(object):
    def __init__(self) -> None:
        self.reg_x = 1
        self.pc = 0
        self._signal_strength: dict[int, int] = {
            key: 0 for key in SIGNAL_STRENGTH_CHECKS
        }

    @property
    def signal_strength(self) -> int:
        return sum(self._signal_strength.values())

    def increment_pc(self, cycles: int) -> None:
        while cycles > 0:
            self.pc += 1
            for check in SIGNAL_STRENGTH_CHECKS[::-1]:
                if self.pc == check:
                    self._signal_strength[check] = check * self.reg_x
                    print(self._signal_strength)
                    break
            cycles -= 1

    def run(self, program: t_program) -> int:
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
        return self.signal_strength


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
    signal_strenght: int = cpu.run(program)

    print(signal_strenght)


if __name__ == "__main__":
    main()
