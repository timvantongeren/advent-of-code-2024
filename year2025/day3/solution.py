import io


def get_highest_joltage(line: str, num_chars: int = 2) -> int:
    num_str = ""
    line = line.replace("\n", "")
    line_len = len(line)
    prev_num_index = -1
    for char_index in range(num_chars):
        this_max_num = None
        for i in range(prev_num_index + 1, line_len - num_chars + char_index + 1):
            this_num = int(line[i])
            if this_max_num is None or this_num > this_max_num:
                this_max_num = this_num
                prev_num_index = i
        num_str += str(this_max_num)
    return int(num_str)


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
    lines = input_stream.readlines()
    joltage_sum = 0
    for line in lines:
        joltage_sum += get_highest_joltage(line, 12)
    return joltage_sum
