from dataclasses import dataclass
import io
from typing import Optional

EMPTY = -1


def get_answer_to_part_1(input_stream: io.StringIO) -> int:
    current_file_id = 0
    filemap = []
    currently_reading_file_block = True
    for char in input_stream.read():
        block_length = int(char)
        if currently_reading_file_block:
            filemap.extend([current_file_id] * block_length)
            current_file_id += 1
            currently_reading_file_block = False
        else:
            filemap.extend([EMPTY] * block_length)
            currently_reading_file_block = True

    N = len(filemap)
    start_index = 0
    end_index = N - 1
    while start_index < end_index:
        start_num = filemap[start_index]
        if start_num != EMPTY:
            start_index += 1
            continue

        end_num = filemap[end_index]
        if end_num == EMPTY:
            end_index -= 1
            continue

        # move
        filemap[start_index] = end_num
        filemap[end_index] = EMPTY

        start_index += 1
        end_index -= 1

    return sum([i * n for i, n in enumerate(filemap) if n != EMPTY])


@dataclass
class Block:
    size: int
    file_id: Optional[int] = None


def get_answer_to_part_2(input_stream: io.StringIO) -> int:
    current_file_id = 0
    filemap: list[Block] = []
    current_index = 0
    currently_reading_file_block = True
    for char in input_stream.read():
        block_length = int(char)
        if currently_reading_file_block:
            filemap.append(Block(block_length, current_file_id))
            current_file_id += 1
            current_index += block_length
            currently_reading_file_block = False
        else:
            filemap.append(Block(block_length))
            current_index += block_length
            currently_reading_file_block = True

    N = len(filemap)
    end_index = N - 1
    while end_index >= 0:
        start_index = 0
        block_to_move = filemap[end_index]
        if block_to_move.file_id is None:
            end_index -= 1
            continue
        while start_index < end_index:
            start_block = filemap[start_index]
            if start_block.file_id is not None or start_block.size < block_to_move.size:
                start_index += 1
                continue

            # move
            # We need to split blocks..
            if block_to_move.size == start_block.size:
                # swap
                filemap[start_index] = block_to_move
                filemap[end_index] = start_block
            else:  # smaller
                filemap = (
                    filemap[:start_index]
                    + [block_to_move, Block(start_block.size - block_to_move.size, None)]
                    + filemap[start_index + 1 :]
                )
                end_index += 1
                filemap[end_index] = Block(block_to_move.size)
            break
        end_index -= 1

    print(filemap)

    current_index = 0
    check_sum = 0
    for block in filemap:
        if block.file_id is None:
            current_index += block.size
            continue
        for i in range(block.size):
            check_sum += (current_index + i) * block.file_id
        current_index += block.size
    return check_sum
