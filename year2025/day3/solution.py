import io


def get_highest_joltage(line: str) -> int:
    current_max = None
    for first_number_idx in range(len(line)):
        first = line[first_number_idx]
        for second_number_idx in range(first_number_idx + 1, len(line)):
            second = line[second_number_idx]
            number = int(f"{first}{second}")
            if not current_max or number > current_max:
                current_max = number
    if current_max is None:
        raise ValueError("WTF")
    return current_max


assert get_highest_joltage("987654321111111") == 98
assert get_highest_joltage("811111111111119") == 89
assert get_highest_joltage("234234234234278") == 78
assert get_highest_joltage("818181911112111") == 92


def get_answer_to_part_1(input_stream: io.StringIO) -> int:
    lines = input_stream.readlines()
    joltage_sum = 0
    for line in lines:
        joltage_sum += get_highest_joltage(line)
    return joltage_sum


def get_answer_to_part_2(input_stream: io.StringIO) -> int:
    pass
