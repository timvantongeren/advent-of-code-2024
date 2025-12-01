from dataclasses import dataclass
from enum import Enum, auto
import io


def parse_set_wires(set_wires_lines: list[str]) -> dict[str, bool]:
    set_wires: dict[str, bool] = {}
    for line in set_wires_lines:
        name, value_part = line.split(": ")
        if "1" in value_part:
            set_wires[name] = True
        elif "0" in value_part:
            set_wires[name] = False
        else:
            raise ValueError(f"Invalid value_part: {value_part}")
    return set_wires


class Operation(Enum):
    AND = auto()
    OR = auto()
    XOR = auto()


@dataclass
class Gate:
    input1: str
    input2: str
    operation: Operation
    output: str

    def evaluate(self, set_wires: dict[str, bool]) -> bool:
        # Outputs into set_wires if available, returns False if not used
        # True if was used
        if not self.input1 in set_wires or not self.input2 in set_wires:
            return False

        in1 = set_wires[self.input1]
        in2 = set_wires[self.input2]
        match self.operation:
            case Operation.AND:
                set_wires[self.output] = in1 and in2
            case Operation.OR:
                set_wires[self.output] = in1 or in2
            case Operation.XOR:
                set_wires[self.output] = in1 != in2
            case _:
                raise ValueError(f"Invalid operation {self.operation}")
        return True


def parse_operations(operation_lines: list[str]) -> list[Gate]:
    gates: list[Gate] = []
    for line in operation_lines:
        line = line.replace("\n", "")
        operation_part, output = line.split(" -> ")
        in1, operation, in2 = operation_part.split(" ")
        match operation:
            case "XOR":
                op = Operation.XOR
            case "OR":
                op = Operation.OR
            case "AND":
                op = Operation.AND
            case _:
                raise ValueError(f"Invalid operation {operation}")
        gates.append(Gate(in1, in2, op, output))
    return gates


@dataclass
class ZNumber:
    index: int
    value: bool


def parse_number_from_z_wires(set_wires: dict[str, bool]) -> int:
    # basically take the sum over 2**z_index for each z wire
    # this is assuming we have all the z indices set
    the_sum = 0
    for wire_name in set_wires:
        if not wire_name.startswith("z"):
            continue
        index = int(wire_name.replace("z", ""))
        the_sum += 2 ** index if set_wires[wire_name] else 0
    return the_sum


def get_answer_to_part_1(input_stream: io.StringIO) -> int:
    lines = input_stream.readlines()
    split_index = lines.index("\n")
    set_wires = parse_set_wires(lines[:split_index])
    gates = parse_operations(lines[split_index + 1 :])
    print(gates)

    while gates:
        # take from the front
        active_gate = gates.pop(0)
        if not active_gate.evaluate(set_wires):
            # put back at the end to first evaluate all others
            gates.append(active_gate)

    return parse_number_from_z_wires(set_wires)


def get_answer_to_part_2(input_stream: io.StringIO) -> int:
    pass
