import io
import itertools
from typing import Callable

from tqdm import tqdm


def parse_line(line: str) -> tuple[int, list[int]]:
    test_part, input_part = line.split(":")
    test_value = int(test_part.strip())
    input_parts = input_part.replace("\n", "").strip().split(" ")
    inputs = [int(i) for i in input_parts]
    return test_value, inputs


assert parse_line("190: 10 19 \n") == (190, [10, 19])

multiplication = lambda nums: nums[0] * nums[1]
addition = lambda nums: nums[0] + nums[1]


def apply_ordered_operations(
    values: list[int], operations: list[Callable[[tuple[int, int]], int]]
) -> int:
    copy_of_values = [i for i in values]
    a = copy_of_values.pop(0)
    while copy_of_values:
        b = copy_of_values.pop(0)
        operation = operations.pop(0)
        a = operation((a, b))
    return a


assert apply_ordered_operations([1, 2, 3], [multiplication, addition]) == 5


def get_answer_to_part_1(input_stream: io.StringIO) -> int:
    lines = input_stream.readlines()
    valid_operations = [multiplication, addition]
    test_value_sum = 0
    for line in lines:
        test_value, inputs = parse_line(line)
        n = len(inputs)
        possible_orders_of_operation = itertools.product(valid_operations, repeat=n)
        for ordered_operations in possible_orders_of_operation:
            ordered_operations = list(ordered_operations)
            value = apply_ordered_operations(inputs, ordered_operations)
            if value == test_value:
                test_value_sum += test_value
                break

    return test_value_sum


concatenation = lambda nums: int(f"{nums[0]}{nums[1]}")

assert concatenation((1, 2)) == 12


def get_answer_to_part_2(input_stream: io.StringIO) -> int:
    lines = input_stream.readlines()
    valid_operations = [multiplication, addition, concatenation]
    test_value_sum = 0
    for line in tqdm(lines):
        test_value, inputs = parse_line(line)
        n = len(inputs)
        possible_orders_of_operation = itertools.product(valid_operations, repeat=n)
        for ordered_operations in possible_orders_of_operation:
            ordered_operations = list(ordered_operations)
            value = apply_ordered_operations(inputs, ordered_operations)
            if value == test_value:
                test_value_sum += test_value
                break

    return test_value_sum
