import io

directions = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]

chars = ["X", "M", "A", "S"]


def get_answer_to_part_1(input_stream: io.StringIO) -> int:
    lines = [l.replace("\n", "") for l in input_stream.readlines()]

    N, K = len(lines), len(lines[0])
    n_xmas = 0
    for i in range(N):
        for j in range(K):
            for d in directions:
                for char_index in range(len(chars)):
                    if i + d[0] * char_index >= N or i + d[0] * char_index < 0:
                        break
                    if j + d[1] * char_index >= K or j + d[1] * char_index < 0:
                        break
                    this_char = lines[i + d[0] * char_index][j + d[1] * char_index]
                    char_to_look_for = chars[char_index]
                    if this_char != char_to_look_for:
                        break
                else:
                    if char_index == len(chars) - 1:
                        # print(f"Found XMAS starting at {i,j}, going {d}")
                        n_xmas += 1
    return n_xmas


def get_answer_to_part_2(input_stream: io.StringIO) -> int:
    lines = [l.replace("\n", "") for l in input_stream.readlines()]

    N, K = len(lines), len(lines[0])
    n_xmas = 0
    for i in range(N):
        for j in range(K):
            this_char = lines[i][j]
            if not this_char == "A":
                continue
            if i + 1 >= N or i - 1 < 0 or j + 1 >= K or j - 1 < 0:
                continue
            diag1 = (lines[i + 1][j + 1], lines[i - 1][j - 1])
            diag2 = (lines[i + 1][j - 1], lines[i - 1][j + 1])
            if not ("M" in diag1 and "S" in diag1):
                continue
            if not ("M" in diag2 and "S" in diag2):
                continue
            n_xmas += 1
    return n_xmas
