from collections import defaultdict
from dataclasses import dataclass
import io
from itertools import groupby


@dataclass
class Direction:
    x: int
    y: int
    name: str


directions = [
    Direction(1, 0, "south"),
    Direction(0, 1, "east"),
    Direction(-1, 0, "north"),
    Direction(0, -1, "west"),
]


@dataclass
class Garden:
    id: int
    name: str
    x: int
    y: int


@dataclass
class GardenCounter:
    counter: int = 0


def map_garden(
    mapped_gardens: dict[int, dict[int, Garden]],
    x: int,
    y: int,
    lines: list[str],
    garden_counter: GardenCounter,
):
    n, m = len(lines), len(lines[0])
    garden_symbol = lines[x][y]
    if not y in mapped_gardens[x]:
        # new garden
        garden = Garden(id=garden_counter.counter, name=garden_symbol, x=x, y=y)
        mapped_gardens[x][y] = garden
    for direction in directions:
        if x + direction.x in mapped_gardens and y + direction.y in mapped_gardens[x + direction.x]:
            # already mapped
            continue
        if not 0 <= (x + direction.x) < n:
            # fence
            continue
        if not 0 <= (y + direction.y) < m:
            # fence
            continue

        next_garden_symbol = lines[x + direction.x][y + direction.y]
        if not next_garden_symbol == garden_symbol:
            # fence
            continue
        # same garden, so we continue that way
        map_garden(mapped_gardens, x + direction.x, y + direction.y, lines, garden_counter)


def get_answer_to_part_1(input_stream: io.StringIO) -> int:
    lines = input_stream.readlines()
    lines = [line.replace("\n", "") for line in lines]

    n, m = len(lines), len(lines[0])
    garden_counter = GardenCounter()
    mapped_gardens: dict[int, dict[int, Garden]] = defaultdict(dict)
    for x in range(n):
        for y in range(m):
            if not y in mapped_gardens[x]:
                # new garden
                garden_counter.counter += 1
                map_garden(mapped_gardens, x, y, lines, garden_counter)

    total_price = 0
    for garden_id in range(garden_counter.counter + 1):
        area = 0
        fence_count = 0
        for x in range(n):
            for y in range(m):
                garden = mapped_gardens[x][y]
                if not garden.id == garden_id:
                    continue
                area += 1
                for direction in directions:
                    if not 0 <= (x + direction.x) < n:
                        # fence
                        fence_count += 1
                    elif not 0 <= (y + direction.y) < m:
                        # fence
                        fence_count += 1
                    elif not mapped_gardens[x + direction.x][y + direction.y].id == garden_id:
                        # fence
                        fence_count += 1
        total_price += area * fence_count

    return total_price


def get_answer_to_part_2(input_stream: io.StringIO) -> int:
    lines = input_stream.readlines()
    lines = [line.replace("\n", "") for line in lines]

    n, m = len(lines), len(lines[0])
    garden_counter = GardenCounter()
    mapped_gardens: dict[int, dict[int, Garden]] = defaultdict(dict)
    for x in range(n):
        for y in range(m):
            if not y in mapped_gardens[x]:
                # new garden
                garden_counter.counter += 1
                map_garden(mapped_gardens, x, y, lines, garden_counter)

    total_price = 0
    for garden_id in range(garden_counter.counter + 1):
        area = 0
        fences: list[tuple[int, int, str]] = []
        for x in range(n):
            for y in range(m):
                garden = mapped_gardens[x][y]
                if not garden.id == garden_id:
                    continue
                area += 1
                for direction in directions:
                    if not 0 <= (x + direction.x) < n:
                        # fence
                        fences.append((x, y, direction.name))
                    elif not 0 <= (y + direction.y) < m:
                        # fence
                        fences.append((x, y, direction.name))
                    elif not mapped_gardens[x + direction.x][y + direction.y].id == garden_id:
                        # fence
                        fences.append((x, y, direction.name))

        sides = 0
        for direction, fence_iter in groupby(sorted(fences, key=lambda x: x[2]), lambda x: x[2]):
            these_fences = list(fence_iter)
            if direction in ["south", "north"]:
                for x, fences_in_row_iter in groupby(
                    sorted(these_fences, key=lambda x: x[0]), lambda x: x[0]
                ):
                    sorted_by_column = sorted(fences_in_row_iter, key=lambda x: x[1])
                    prev_y = -10  # just far away so doesn't trigger
                    for _, y, _ in sorted_by_column:
                        if y - prev_y == 1:
                            # same side
                            pass
                        else:
                            # new side
                            sides += 1
                        prev_y = y
            else:
                for y, fences_in_row_iter in groupby(
                    sorted(these_fences, key=lambda x: x[1]), lambda x: x[1]
                ):
                    sorted_by_column = sorted(fences_in_row_iter, key=lambda x: x[0])
                    prev_x = -10  # just far away so doesn't trigger
                    for x, _, _ in sorted_by_column:
                        if x - prev_x == 1:
                            # same side
                            pass
                        else:
                            # new side
                            sides += 1
                        prev_x = x
        # print(area, sides, garden_id)
        total_price += area * sides

    return total_price
