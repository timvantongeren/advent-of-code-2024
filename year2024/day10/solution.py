from dataclasses import dataclass
import io

directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]


@dataclass
class PeakCounter:
    peaks: set[tuple[int, int]]

    def add(self, peak: tuple[int, int]):
        self.peaks.add(peak)

    def number_of_peaks(self) -> int:
        return len(self.peaks)


@dataclass
class PeakCounter2:
    peak_count: int = 0

    def add(self, peak: tuple[int, int]):
        self.peak_count += 1

    def number_of_peaks(self) -> int:
        return self.peak_count


def explore(
    starting_location: tuple[int, int],
    the_map: list[list[int]],
    peak_counter: PeakCounter | PeakCounter2,
):
    n, m = len(the_map), len(the_map[0])
    current_height = the_map[starting_location[0]][starting_location[1]]
    for direction in directions:
        next_location = (starting_location[0] + direction[0], starting_location[1] + direction[1])
        if not (0 <= next_location[0] <= n - 1) or not (0 <= next_location[1] <= m - 1):
            continue
        next_height = the_map[next_location[0]][next_location[1]]
        if not (next_height - current_height) == 1:
            continue
        elif next_height == 9:
            peak_counter.add(next_location)
            continue
        else:
            explore(next_location, the_map, peak_counter)


def get_answer_to_part_1(input_stream: io.StringIO) -> int:
    lines = input_stream.readlines()
    the_map = [[int(i) for i in line.replace("\n", "")] for line in lines]
    n, m = len(the_map), len(the_map[0])
    trailheads = [(i, j) for i in range(n) for j in range(m) if the_map[i][j] == 0]
    total = 0
    for trailhead in trailheads:
        peak_counter = PeakCounter(set())
        explore(trailhead, the_map, peak_counter)
        total += peak_counter.number_of_peaks()
    return total


def get_answer_to_part_2(input_stream: io.StringIO) -> int:
    lines = input_stream.readlines()
    the_map = [[int(i) for i in line.replace("\n", "")] for line in lines]
    n, m = len(the_map), len(the_map[0])
    trailheads = [(i, j) for i in range(n) for j in range(m) if the_map[i][j] == 0]
    total = 0
    for trailhead in trailheads:
        peak_counter = PeakCounter2()
        explore(trailhead, the_map, peak_counter)
        total += peak_counter.number_of_peaks()
    return total
