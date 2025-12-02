import io


def id_is_valid(id: int) -> bool:
    id_as_str = str(id)
    if len(id_as_str) % 2 != 0:
        # not even number of digits
        return True
    half_way = int(len(id_as_str) / 2)
    start_slice = id_as_str[:half_way]
    start_and_end_same = id_as_str.endswith(start_slice)
    return not start_and_end_same


assert not id_is_valid(55)
assert not id_is_valid(6464)
assert not id_is_valid(123123)
assert id_is_valid(101)
assert id_is_valid(7)
assert id_is_valid(123451234)


def get_answer_to_part_1(input_stream: io.StringIO) -> int:
    whole_input = input_stream.read()
    cleaned_input = whole_input.replace("\n", "")
    invalid_id_sum = 0
    for input_range in cleaned_input.split(","):
        raw_lower, raw_upper = input_range.split("-")
        lower, upper = int(raw_lower), int(raw_upper)
        for id_to_check in range(lower, upper + 1):
            if id_is_valid(id_to_check):
                continue
            invalid_id_sum += id_to_check
    return invalid_id_sum


def get_answer_to_part_2(input_stream: io.StringIO) -> int:
    pass
