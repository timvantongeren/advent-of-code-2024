from dataclasses import dataclass, field
import io

from tqdm import tqdm


@dataclass
class Computer:
    a: int
    b: int
    c: int

    program: list[int]

    instruction_pointer: int = 0
    output: list[int] = field(default_factory=list)

    @property
    def opcode(self) -> int:
        if self.instruction_pointer >= len(self.program):
            return -1
        return self.program[self.instruction_pointer]

    @property
    def operand(self) -> int:
        if (self.instruction_pointer + 1) >= len(self.program):
            return -1
        return self.program[(self.instruction_pointer + 1)]

    def map_combo_operand(self, combo_operand: int) -> int:
        if combo_operand < 4:
            return combo_operand
        if combo_operand == 4:
            return self.a
        if combo_operand == 5:
            return self.b
        if combo_operand == 6:
            return self.c
        if combo_operand == 7:
            raise ValueError("Invalid combo operand")
        raise ValueError("Invalid operand")

    def adv(self, combo_operand: int):
        operand = self.map_combo_operand(combo_operand)
        numerator = self.a
        denominator = 2**operand
        div = numerator // denominator
        self.a = div

    def bxl(self, literal_operand: int):
        self.b = self.b ^ literal_operand

    def bst(self, combo_operand: int):
        operand = self.map_combo_operand(combo_operand)
        val = operand % 8
        self.b = val

    def jnz(self, literal_operand: int):
        if self.a == 0:
            return
        if literal_operand == self.instruction_pointer:
            return
        self.instruction_pointer = literal_operand
        # to counteract the no jump
        self.instruction_pointer -= 2

    def bxc(self, _: int):
        xor = self.b ^ self.c
        self.b = xor

    def out(self, combo_operand: int):
        operand = self.map_combo_operand(combo_operand)
        out = operand % 8
        self.output.append(out)

    def bdv(self, combo_operand: int):
        operand = self.map_combo_operand(combo_operand)
        numerator = self.a
        denominator = 2**operand
        div = numerator // denominator
        self.b = div

    def cdv(self, combo_operand: int):
        operand = self.map_combo_operand(combo_operand)
        numerator = self.a
        denominator = 2**operand
        div = numerator // denominator
        self.c = div

    def run_next_operation(self):
        match self.opcode:
            case 0:
                self.adv(self.operand)
            case 1:
                self.bxl(self.operand)
            case 2:
                self.bst(self.operand)
            case 3:
                self.jnz(self.operand)
            case 4:
                self.bxc(self.operand)
            case 5:
                self.out(self.operand)
            case 6:
                self.bdv(self.operand)
            case 7:
                self.cdv(self.operand)
        self.instruction_pointer += 2

    def run(self) -> list[int]:
        while self.instruction_pointer < len(self.program):
            self.run_next_operation()
        return self.output


def initialize_computer(lines: list[str]) -> Computer:
    lines = [l.replace("\n", "") for l in lines]
    a = int(lines[0].split(":")[-1])
    b = int(lines[1].split(":")[-1])
    c = int(lines[2].split(":")[-1])

    program = [int(i) for i in lines[4].split(":")[-1].split(",")]
    return Computer(a, b, c, program)


def get_answer_to_part_1(input_stream: io.StringIO) -> int:
    lines = input_stream.readlines()
    computer = initialize_computer(lines)
    output = computer.run()
    return ",".join([str(i) for i in output])  # type: ignore


def output_can_be_program(output: list[int], program: list[int]):
    if len(output) > len(program):
        return False
    for i in range(len(output)):
        if output[i] != program[i]:
            return False
    return True


def output_is_program(output: list[int], program: list[int]):
    if not len(output) == len(program):
        return False
    return all([o == p for o, p in zip(output, program)])


def get_answer_to_part_2(input_stream: io.StringIO) -> int:
    lines = input_stream.readlines()

    for initial_a in tqdm([32**15 - 1, 32**16 - 1]):
        computer = initialize_computer(lines)
        computer.a = initial_a
        while computer.instruction_pointer < len(computer.program) and output_can_be_program(
            computer.output, computer.program
        ):
            computer.run_next_operation()
        if output_is_program(computer.output, computer.program):
            return initial_a
    raise ValueError(f"Did not find solution after")
