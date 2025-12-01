import io


def get_towels(line: str) -> set[str]:
    line = line.replace("\n", "").replace(" ", "")
    return set(line.split(","))


def get_patterns(lines: list[str]) -> list[str]:
    return [l.replace("\n", "") for l in lines]


def pattern_is_possible_with(towels: set[str], pattern: str, longest_towel_len: int) -> bool:
    pattern_start_index = 0
    pattern_len = len(pattern)
    while pattern_start_index < pattern_len:
        for offset in range(1, longest_towel_len + 1):
            pattern_part = pattern[pattern_start_index : pattern_start_index + offset]
            if pattern_part in towels:
                # this might not immediately be the right one
                pattern_start_index += offset
                break
        else:
            return False
    return True


assert pattern_is_possible_with(set(["ab", "c"]), "abcab", 2)
assert pattern_is_possible_with(set(["bac", "ca"]), "cabacca", 3)
assert not pattern_is_possible_with(set(["bac", "ca", "d"]), "dbcabac", 3)
assert pattern_is_possible_with(set(["r", "br", "rb", "bwu", "g", "wr", "gb", "b"]), "bwurrg", 3)


def get_answer_to_part_1(input_stream: io.StringIO) -> int:
    lines = input_stream.readlines()
    towels = get_towels(lines[0])
    print(towels)
    longest_towel_len = max([len(t) for t in towels])
    print(longest_towel_len)
    patterns = get_patterns(lines[2:])

    possible = 0
    for pattern in patterns:
        is_possible = pattern_is_possible_with(towels, pattern, longest_towel_len)
        if is_possible:
            print(f"Pattern {pattern} is possible")
            possible += 1
        else:
            print(f"Impossible pattern {pattern}")
    return possible


def get_answer_to_part_2(input_stream: io.StringIO) -> int:
    pass
