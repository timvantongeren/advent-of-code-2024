from collections import defaultdict
import io
from tqdm import tqdm


def is_even(num: int) -> bool:
    return num % 2 == 0


def evolve(number: int) -> list[int]:
    if number == 0:
        return [1]
    number_as_string = str(number)
    number_length = len(number_as_string)
    if is_even(number_length):
        halfway_index = int(number_length / 2)
        return [int(number_as_string[:halfway_index]), int(number_as_string[halfway_index:])]
    return [number * 2024]


assert evolve(0) == [1]
assert evolve(10) == [1, 0]
assert evolve(100) == [202400]
assert evolve(1000) == [10, 0]


def replace(the_list: list[int], index: int, replacement: list[int]) -> list[int]:
    return the_list[:index] + replacement + the_list[index + 1 :]


assert replace([1, 2, 3, 4, 5], 2, [6, 7]) == [1, 2, 6, 7, 4, 5]


def get_answer_to_part_1(input_stream: io.StringIO) -> int:
    line = input_stream.readline().strip()
    numbers = [int(i) for i in line.split(" ")]
    for _blink in tqdm(range(25)):
        i = 0
        while i < len(numbers):
            replacement = evolve(numbers[i])
            numbers = replace(numbers, i, replacement)
            i += len(replacement)

        # in test case
        # if _blink == 5:
        # assert len(numbers) == 22
    return len(numbers)


def get_answer_to_part_2(input_stream: io.StringIO) -> int:
    # really only matters what a number evolves into
    line = input_stream.readline().strip()
    numbers = [int(i) for i in line.split(" ")]
    cache_in_out: dict[int, list[int]] = {}
    current = {}
    for n in numbers:
        if not n in current:
            current[n] = 1
        else:
            current[n] += 1
    for _blink in tqdm(range(75)):
        next = {}
        for n in current:
            if n in cache_in_out:
                evolved = cache_in_out[n]
            else:
                evolved = evolve(n)
                cache_in_out[n] = evolved
            for e in evolved:
                if e not in next:
                    next[e] = current[n]
                else:
                    next[e] += current[n]
        current = {k: next[k] for k in next}
    return sum(current[k] for k in current)
