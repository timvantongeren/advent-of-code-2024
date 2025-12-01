import matplotlib.pyplot as plt
from dataclasses import dataclass
import numpy as np
from enum import Enum, auto
import io


class Tile(Enum):
    WALL = auto()
    CRATE = auto()
    AIR = auto()
    SHARK = auto()


def parse_warehouse(warehouse_lines: list[str]) -> list[list[Tile]]:
    warehouse: list[list[Tile]] = []
    for line in warehouse_lines:
        this_line = []
        for char in line:
            match char:
                case "#":
                    this_line.append(Tile.WALL)
                case ".":
                    this_line.append(Tile.AIR)
                case "O":
                    this_line.append(Tile.CRATE)
                case "@":
                    this_line.append(Tile.SHARK)
                case "\n":
                    pass
                case _:
                    raise ValueError(f"Unknown symbol {char}")
        warehouse.append(this_line)
    return warehouse


@dataclass
class Direction:
    x: int
    y: int


def parse_moves(move_lines: list[str]) -> list[Direction]:
    moves: list[Direction] = []
    for line in move_lines:
        for char in line:
            match char:
                case "<":
                    moves.append(Direction(0, -1))
                case "^":
                    moves.append(Direction(-1, 0))
                case ">":
                    moves.append(Direction(0, 1))
                case "v":
                    moves.append(Direction(1, 0))
                case "\n":
                    pass
                case _:
                    raise ValueError(f"Unknown move {char}")
    return moves


@dataclass
class Location:
    x: int
    y: int


def find_shark(warehouse: list[list[Tile]]) -> Location:
    for x in range(len(warehouse)):
        for y in range(len(warehouse[0])):
            if warehouse[x][y] == Tile.SHARK:
                return Location(x, y)
    raise ValueError("Can't find shark")


def get_gps_coordinates(warehouse: list[list[Tile]]) -> int:
    coordinate_sum = 0
    for x, row in enumerate(warehouse):
        for y, tile in enumerate(row):
            if tile == Tile.CRATE:
                coords = 100 * x + y
                coordinate_sum += coords
    return coordinate_sum


def get_answer_to_part_1(input_stream: io.StringIO) -> int:
    lines = input_stream.readlines()
    empty_line = lines.index("\n")
    warehouse_lines = lines[:empty_line]
    move_lines = lines[empty_line + 1 :]

    warehouse = parse_warehouse(warehouse_lines)
    moves = parse_moves(move_lines)

    shark_location = find_shark(warehouse)
    for move in moves:
        end_of_straight = Location(shark_location.x, shark_location.y)
        # plt.imshow([[t.value for t in row] for row in warehouse])
        # plt.show()
        while warehouse[end_of_straight.x][end_of_straight.y] in [Tile.SHARK, Tile.CRATE]:
            end_of_straight.x += move.x
            end_of_straight.y += move.y
        # At this point we're looking at either air or wall
        if warehouse[end_of_straight.x][end_of_straight.y] == Tile.WALL:
            continue

        # Now we have air at the end of a straight, so it can be pushed.
        # That means that everything from the shark location to
        # the end of straight - 1 move moves 1 tile in the location of the move.
        while end_of_straight.x != shark_location.x or end_of_straight.y != shark_location.y:
            warehouse[end_of_straight.x][end_of_straight.y] = warehouse[end_of_straight.x - move.x][
                end_of_straight.y - move.y
            ]
            end_of_straight.x -= move.x
            end_of_straight.y -= move.y

        # Then as we moved the original location of the share becomes air
        warehouse[shark_location.x][shark_location.y] = Tile.AIR

        # And lastly we need to move the pointer to the shark location
        shark_location.x += move.x
        shark_location.y += move.y

    return get_gps_coordinates(warehouse)


def expand_warehouse_lines(warehouse_lines: list[str]) -> list[str]:
    expanded_lines = []
    for line in warehouse_lines:
        new_line = line.replace("\n", "")
        new_line = new_line.replace("#", "##")
        new_line = new_line.replace("O", "[]")
        new_line = new_line.replace(".", "..")
        new_line = new_line.replace("@", "@.")
        expanded_lines.append(new_line)
    return expanded_lines


def get_walls_from_expanded_lines(expanded_warehouse_lines: list[str]) -> list[Location]:
    locations = []
    for x, line in enumerate(expanded_warehouse_lines):
        for y, char in enumerate(line):
            if char == "#":
                locations.append(Location(x, y))

    return locations


def find_shark2(expanded_warehouse_lines: list[str]) -> Location:
    for x, line in enumerate(expanded_warehouse_lines):
        for y, char in enumerate(line):
            if char == "@":
                return Location(x, y)
    raise ValueError("Can't find shark")


@dataclass
class Box:
    id: int
    loc1: Location
    loc2: Location

    def __hash__(self) -> int:
        return self.id

    def move(self, direction: Direction):
        self.loc1.x += direction.x
        self.loc1.y += direction.y
        self.loc2.x += direction.x
        self.loc2.y += direction.y


def get_boxes_from_expanded_lines(expanded_warehouse_lines: list[str]) -> list[Box]:
    boxes = []
    box_id = 0
    for x, line in enumerate(expanded_warehouse_lines):
        for y, char in enumerate(line):
            if char == "[":
                boxes.append(Box(box_id, Location(x, y), Location(x, y + 1)))
                box_id += 1
    return boxes


def visualize(shark: Location, boxes: list[Box], walls: list[Location], n_x: int, n_y: int):
    grid = np.zeros((n_x, n_y))
    grid[shark.x][shark.y] = 1
    for box in boxes:
        grid[box.loc1.x][box.loc1.y] = 2
        grid[box.loc2.x][box.loc2.y] = 2

    for wall in walls:
        grid[wall.x][wall.y] = -1

    plt.imshow(grid)
    plt.show()


def get_ahead_box(location: Location, move: Direction, boxes: list[Box]) -> Box | None:
    ahead = Location(location.x + move.x, location.y + move.y)
    for box in boxes:
        if box.loc1 == ahead:
            return box
        if box.loc2 == ahead:
            return box
    return None


def iteratively_find_connected_boxes(
    location: Location,
    move: Direction,
    boxes: list[Box],
    boxes_in_front: set[Box],
    n_x: int,
    n_y: int,
):
    if ahead_box := get_ahead_box(Location(location.x, location.y), move, boxes):
        if ahead_box in boxes_in_front:
            return
        boxes_in_front.add(ahead_box)
        for loc in [ahead_box.loc1, ahead_box.loc2]:
            if (0 <= loc.x < n_x) and (0 <= loc.y < n_y):
                iteratively_find_connected_boxes(loc, move, boxes, boxes_in_front, n_x, n_y)


def all_boxes_free_to_move(boxes: set[Box], walls: list[Location], move: Direction) -> bool:
    for box in boxes:
        loc1_moved = Location(box.loc1.x + move.x, box.loc1.y + move.y)
        loc2_moved = Location(box.loc2.x + move.x, box.loc2.y + move.y)
        if loc1_moved in walls or loc2_moved in walls:
            return False
    return True


def get_answer_to_part_2(input_stream: io.StringIO) -> int:
    # oke dus.
    # we hebben een set met coords van de muren nodig.
    # Blokken gaan we als Object encoden met 2 locaties.
    # Dan, collision check, raakt de shark een box: if yes, check if box can move.
    # box can move als er of lucht boven zit, of een box die ook kan moven, dus recursief vooruit checken.
    # Dan als er gemoved kan worden, vanaf de verste alle items die moven 1 stap in de richting moven.
    # Ez.
    lines = input_stream.readlines()
    empty_line = lines.index("\n")
    warehouse_lines = lines[:empty_line]
    move_lines = lines[empty_line + 1 :]

    moves = parse_moves(move_lines)
    expanded_warehouse_lines = expand_warehouse_lines(warehouse_lines)
    walls = get_walls_from_expanded_lines(expanded_warehouse_lines)
    boxes = get_boxes_from_expanded_lines(expanded_warehouse_lines)
    shark = find_shark2(expanded_warehouse_lines)

    n_x = len(expanded_warehouse_lines)
    n_y = len(expanded_warehouse_lines[0])

    visualize_every_n = 500
    if visualize_every_n:
        plt.title(f"Step {0}/{len(moves)}")
        visualize(shark, boxes, walls, n_x, n_y)
    for i, move in enumerate(moves):
        boxes_in_front: set[Box] = set()
        iteratively_find_connected_boxes(shark, move, boxes, boxes_in_front, n_x, n_y)
        ahead = Location(shark.x + move.x, shark.y + move.y)
        if boxes_in_front:
            # move if all free to move, aka non of them have any piece of wall in front
            if all_boxes_free_to_move(boxes_in_front, walls, move):
                shark = ahead
                for box in boxes_in_front:
                    box.move(move)
        else:
            if any([w == ahead for w in walls]):
                # no move
                pass
            else:
                # air ahead
                shark = ahead

        if visualize_every_n and i % visualize_every_n == 0:
            plt.title(f"Step {i+1}/{len(moves)}")
            visualize(shark, boxes, walls, n_x, n_y)

    gps_sum = 0
    for box in boxes:
        gps_sum += box.loc1.x * 100 + box.loc1.y
    return gps_sum
