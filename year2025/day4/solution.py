from enum import StrEnum
import io


class BoardTile(StrEnum):
    EMPTY = "."
    PAPER_ROLL = "@"


def get_answer_to_part_1(input_stream: io.StringIO) -> int:
    lines = input_stream.readlines()
    lines = [l.replace("\n", "") for l in lines]
    n = len(lines)
    m = len(lines[0])
    movable_rolls = 0
    for i in range(n):
        for j in range(m):
            this_tile = lines[i][j]
            if this_tile == BoardTile.EMPTY:
                continue

            paper_count = 0
            for i_offset in [-1, 0, 1]:
                for j_offset in [-1, 0, 1]:
                    if i_offset == 0 and j_offset == 0:
                        continue
                    adjacent_i = i + i_offset
                    adjacent_j = j + j_offset
                    if adjacent_i < 0 or adjacent_i >= n or adjacent_j < 0 or adjacent_j >= m:
                        # Outside of the board
                        continue
                    adjacent_tile = lines[adjacent_i][adjacent_j]
                    if adjacent_tile == BoardTile.PAPER_ROLL:
                        paper_count += 1

            if paper_count < 4:
                movable_rolls += 1

    return movable_rolls


assert "abc"[:1] + "d" + "abc"[1 + 1 :] == "adc"


def round_of_clearing(lines: list[str]) -> list[str]:
    n = len(lines)
    m = len(lines[0])
    movable_rolls = 0
    for i in range(n):
        for j in range(m):
            this_tile = lines[i][j]
            if this_tile == BoardTile.EMPTY:
                continue

            paper_count = 0
            for i_offset in [-1, 0, 1]:
                for j_offset in [-1, 0, 1]:
                    if i_offset == 0 and j_offset == 0:
                        continue
                    adjacent_i = i + i_offset
                    adjacent_j = j + j_offset
                    if adjacent_i < 0 or adjacent_i >= n or adjacent_j < 0 or adjacent_j >= m:
                        # Outside of the board
                        continue
                    adjacent_tile = lines[adjacent_i][adjacent_j]
                    if adjacent_tile == BoardTile.PAPER_ROLL:
                        paper_count += 1

            if paper_count < 4:

                lines[i] = lines[i][:j] + BoardTile.EMPTY + lines[i][j + 1 :]
    return lines


def count_paper(lines: list[str]) -> int:
    return sum([sum([char == BoardTile.PAPER_ROLL for char in line]) for line in lines])


def get_answer_to_part_2(input_stream: io.StringIO) -> int:
    lines = input_stream.readlines()
    lines = [l.replace("\n", "") for l in lines]
    original_paper_count = count_paper(lines)
    prev_paper_count = None
    while True:
        if prev_paper_count == count_paper(lines):
            return original_paper_count - prev_paper_count
        prev_paper_count = count_paper(lines)
        lines = round_of_clearing(lines)
