from collections import defaultdict
from dataclasses import dataclass
import io
import sys

sys.setrecursionlimit(10_000)


@dataclass(eq=True, frozen=True)
class Tile:
    x: int
    y: int

    def __add__(self, other):
        return Tile(self.x + other.x, self.y + other.y)


@dataclass
class Map:
    walls: set[Tile]
    deer: Tile
    target: Tile


def parse_map(lines: list[str]) -> Map:
    walls = set()
    deer = None
    target = None
    for x, line in enumerate(lines):
        for y, char in enumerate(line):
            match char:
                case "#":
                    walls.add(Tile(x, y))
                case "S":
                    deer = Tile(x, y)
                case "E":
                    target = Tile(x, y)

    if deer is None:
        raise ValueError("Couldn't find deer")
    if target is None:
        raise ValueError("Couldn't find target")

    return Map(walls, deer, target)


directions = [Tile(1, 0), Tile(-1, 0), Tile(0, 1), Tile(0, -1)]


def continue_if_cheaper_than_seen(
    current_tile, current_dir, map, tiles_crossed_in_direction_at_cost, target
) -> list[tuple[Tile, Tile]]:
    next_tiles = []
    for dir in directions:
        next_tile = current_tile + dir
        if next_tile in map.walls:
            continue

        current_cost = tiles_crossed_in_direction_at_cost.get((current_tile, current_dir), 0)
        if dir == current_dir or current_dir is None:
            next_cost = current_cost + 1
        else:
            next_cost = current_cost + 1000 + 1

        if next_cost < tiles_crossed_in_direction_at_cost.get((next_tile, dir), 100_000_000):
            tiles_crossed_in_direction_at_cost[(next_tile, dir)] = next_cost
            if next_tile == target:
                return []
            next_tiles.append((next_tile, dir))
    return next_tiles


def get_answer_to_part_1(input_stream: io.StringIO) -> int:
    lines = input_stream.readlines()
    map = parse_map(lines)

    deer = map.deer
    tiles_crossed_in_direction_at_cost: dict[tuple[Tile, Tile], int] = {}

    next_tiles: list[tuple[Tile, Tile]] = [(Tile(deer.x, deer.y), Tile(0, 1))]
    while next_tiles:
        tile, dir = next_tiles.pop()
        to_go = continue_if_cheaper_than_seen(
            tile,
            dir,
            map,
            tiles_crossed_in_direction_at_cost,
            map.target,
        )
        next_tiles.extend(to_go)

    costs_of_target = []
    for tile, dir in tiles_crossed_in_direction_at_cost:
        if tile != map.target:
            continue
        costs_of_target.append(tiles_crossed_in_direction_at_cost[(tile, dir)])
    return min(costs_of_target)


def get_answer_to_part_2(input_stream: io.StringIO) -> int:
    pass
