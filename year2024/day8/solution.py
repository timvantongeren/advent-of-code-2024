from collections import defaultdict
import io


def get_answer_to_part_1(input_stream: io.StringIO) -> int:
    # General idea is that the vector between 2 antennas should be applied again
    # to find the point which is twice the distance between the antennas.
    # Just loop over all points, loop over the same frequency points,
    # apply their vectors again, and store that set.
    # By simply looping over all points instead of the pairs that
    # immediately finds the other side as well.
    lines = input_stream.readlines()
    frequency_towers: dict[str, set[tuple[int, int]]] = defaultdict(set)
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == ".":
                continue
            frequency_towers[char].add((i, j))
    max_i, max_j = i, j

    antinodes: set[tuple[int, int]] = set()
    for frequency in frequency_towers:
        towers = frequency_towers[frequency]
        for tower in towers:
            for other_tower in towers:
                if tower == other_tower:
                    continue
                d_i = tower[0] - other_tower[0]
                d_j = tower[1] - other_tower[1]
                # Doesn't really matter if this is the right way around, as long as it's consistent
                antinode_i = tower[0] + d_i
                antinode_j = tower[1] + d_j
                if (0 <= antinode_i <= max_i) and (0 <= antinode_j <= max_j):
                    antinodes.add((antinode_i, antinode_j))
    return len(antinodes)


def get_answer_to_part_2(input_stream: io.StringIO) -> int:
    # Okay so now we have to apply the difference vector multiple times,
    # as long as the result is within bounds.
    lines = input_stream.readlines()
    frequency_towers: dict[str, set[tuple[int, int]]] = defaultdict(set)
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == ".":
                continue
            frequency_towers[char].add((i, j))
    max_i, max_j = i, j

    antinodes: set[tuple[int, int]] = set()
    for frequency in frequency_towers:
        towers = frequency_towers[frequency]
        for tower in towers:
            for other_tower in towers:
                if tower == other_tower:
                    continue
                multiplier = 0
                d_i = tower[0] - other_tower[0]
                d_j = tower[1] - other_tower[1]
                # Doesn't really matter if this is the right way around, as long as it's consistent
                antinode_i = tower[0] + d_i * multiplier
                antinode_j = tower[1] + d_j * multiplier
                while (0 <= antinode_i <= max_i) and (0 <= antinode_j <= max_j):
                    antinodes.add((antinode_i, antinode_j))
                    multiplier += 1
                    d_i = tower[0] - other_tower[0]
                    d_j = tower[1] - other_tower[1]
                    # Doesn't really matter if this is the right way around, as long as it's consistent
                    antinode_i = tower[0] + d_i * multiplier
                    antinode_j = tower[1] + d_j * multiplier
    return len(antinodes)
