import io


def parse_input(lines: list[str]) -> list[tuple[tuple[int, int], tuple[int, int], tuple[int, int]]]:
    machines = []
    for block_index in range((len(lines) + 1) // 4):
        machine_a_line = lines[block_index * 4].replace("\n", "")
        machine_b_line = lines[block_index * 4 + 1].replace("\n", "")
        prize_line = lines[block_index * 4 + 2].replace("\n", "")
        a_x = int(machine_a_line.replace("Button A: X", "").split(",")[0])
        a_y = int(machine_a_line.split(" Y")[1])
        b_x = int(machine_b_line.replace("Button B: X", "").split(",")[0])
        b_y = int(machine_b_line.split(" Y")[1])
        p_x = int(prize_line.replace("Prize: X=", "").split(",")[0])
        p_y = int(prize_line.split(" Y=")[1])
        machines.append(((a_x, a_y), (b_x, b_y), (p_x, p_y)))
    return machines


def get_answer_to_part_1(input_stream: io.StringIO) -> int:
    lines = input_stream.readlines()
    machines = parse_input(lines)
    price = 0
    for (a_x, a_y), (b_x, b_y), (p_x, p_y) in machines:
        det = a_x * b_y - b_x * a_y
        if det == 0:
            # Non invertable, so no solution
            continue

        a_numerator = b_y * p_x - p_y * b_x
        b_numerator = a_x * p_y - a_y * p_x

        if a_numerator % det != 0:
            # non integer
            continue
        if b_numerator % det != 0:
            # non integer
            continue

        a = a_numerator // det
        b = b_numerator // det

        price += 3 * a + b
    return price


def get_answer_to_part_2(input_stream: io.StringIO) -> int:
    lines = input_stream.readlines()
    machines = parse_input(lines)
    price = 0
    for (a_x, a_y), (b_x, b_y), (p_x, p_y) in machines:
        p_x += 10000000000000
        p_y += 10000000000000
        det = a_x * b_y - b_x * a_y
        if det == 0:
            # Non invertable, so no solution
            continue

        a_numerator = b_y * p_x - p_y * b_x
        b_numerator = a_x * p_y - a_y * p_x

        if a_numerator % det != 0:
            # non integer
            continue
        if b_numerator % det != 0:
            # non integer
            continue

        a = a_numerator // det
        b = b_numerator // det

        price += 3 * a + b
    return price
