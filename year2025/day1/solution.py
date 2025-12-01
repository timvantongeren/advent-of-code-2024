import io


assert 1107 % 100 == 7
assert -327 % 100 == 73


def get_answer_to_part_1(input_stream: io.StringIO) -> int:
    lines = input_stream.readlines()
    location = 50
    zero_count = 0
    for instruction in lines:
        side = instruction[0]
        amount = int(instruction[1:].replace("\n", ""))
        if side == "L":
            location -= amount
        else:
            location += amount
        location = location % 100
        if location == 0:
            zero_count += 1
    print(f"Final location is {location}")
    return zero_count


def get_answer_to_part_2(input_stream: io.StringIO) -> int:
    lines = input_stream.readlines()
    location = 50
    zero_count = 0
    for instruction in lines:
        side = instruction[0]
        amount = int(instruction[1:].replace("\n", ""))
        if side == "L":
            for _ in range(amount):
                location -= 1
                if location % 100 == 0:
                    zero_count += 1
        else:
            for _ in range(amount):
                location += 1
                if location % 100 == 0:
                    zero_count += 1
        location = location % 100
    print(f"Final location is {location}")
    return zero_count
