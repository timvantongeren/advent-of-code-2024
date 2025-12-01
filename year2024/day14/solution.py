from dataclasses import dataclass
import io
import matplotlib.pyplot as plt
from tqdm import tqdm
from itertools import product


@dataclass(eq=True, frozen=True)
class Coordinates:
    x: int
    y: int


@dataclass
class Robot:
    position: Coordinates
    velocity: Coordinates

    def move(self, max_x: int, max_y: int):
        new_x = self.position.x + self.velocity.x
        if new_x < 0:
            new_x = max_x + new_x
        if new_x >= max_x:
            new_x -= max_x
        new_y = self.position.y + self.velocity.y
        if new_y < 0:
            new_y = max_y + new_y
        if new_y >= max_y:
            new_y -= max_y
        self.position = Coordinates(new_x, new_y)


def test_wrap():
    robot = Robot(Coordinates(2, 4), Coordinates(2, -3))
    robot.move(11, 7)
    expected_position = Coordinates(4, 1)
    assert robot.position == expected_position
    robot.move(11, 7)
    expected_position = Coordinates(6, 5)
    assert robot.position == expected_position


test_wrap()


def parse_input(lines: list[str]) -> list[Robot]:
    robots: list[Robot] = []
    for line in lines:
        line = line.replace("\n", "")
        position = Coordinates(*(int(c) for c in line.replace("p=", "").split(" ")[0].split(",")))
        velocity = Coordinates(*(int(c) for c in line.split("v=")[1].split(",")))
        robots.append(Robot(position, velocity))
    return robots


def get_answer_to_part_1(input_stream: io.StringIO) -> int:
    lines = input_stream.readlines()
    robots = parse_input(lines)
    max_x, max_y = 101, 103
    middle_x_index = max_x // 2
    middle_y_index = max_y // 2
    quadrant_count = [0, 0, 0, 0]
    for robot in robots:
        for _ in range(100):
            robot.move(max_x, max_y)

        if robot.position.x < middle_x_index and robot.position.y < middle_y_index:
            quadrant_count[0] += 1
        if robot.position.x > middle_x_index and robot.position.y < middle_y_index:
            quadrant_count[1] += 1
        if robot.position.x < middle_x_index and robot.position.y > middle_y_index:
            quadrant_count[2] += 1
        if robot.position.x > middle_x_index and robot.position.y > middle_y_index:
            quadrant_count[3] += 1
    return quadrant_count[0] * quadrant_count[1] * quadrant_count[2] * quadrant_count[3]


def bottom_of_tree_visible(grid, max_y) -> bool:
    index_of_bottom = max_y - 3
    return all(grid[index_of_bottom])


def get_connected_coordinates(coords: Coordinates) -> set[Coordinates]:
    return set(
        [
            Coordinates(coords.x + x_offset, coords.y + y_offset)
            for x_offset, y_offset in product([-1, 0, 1], repeat=2)
            if not (x_offset == 0 and y_offset == 0)
        ]
    )


def might_be_tree(positions: set[Coordinates]) -> bool:
    might_be_tree = False
    for position in positions:
        connected = get_connected_coordinates(position)
        if connected.intersection(positions):
            # might be tree
            might_be_tree = True
        else:
            might_be_tree = False
            break
    return might_be_tree


def tree_score(positions: set[Coordinates]) -> float:
    return sum(
        [
            len(get_connected_coordinates(position).intersection(positions)) > 0
            for position in positions
        ]
    ) / len(positions)
    # for position in positions:
    #     connected = get_connected_coordinates(position)
    #     if connected.intersection(positions):
    #         # might be tree, as node is connected
    #         score += 1
    # return score / len(positions)


assert might_be_tree(set([Coordinates(0, 0), Coordinates(0, 1)]))
assert might_be_tree(set([Coordinates(0, 0), Coordinates(1, 1)]))
assert not might_be_tree(set([Coordinates(0, 0), Coordinates(0, 2)]))
assert might_be_tree(set([Coordinates(0, 0), Coordinates(0, 0), Coordinates(0, 1)]))


def get_answer_to_part_2(input_stream: io.StringIO) -> int:
    lines = input_stream.readlines()
    robots = parse_input(lines)
    max_x, max_y = 101, 103
    # max_x, max_y = 11, 7
    for t in tqdm(range(100000000)):
        for robot in robots:
            robot.move(max_x, max_y)
        positions = set(r.position for r in robots)
        score = tree_score(positions)
        if score < 0.70:
            continue
        # elif not might_be_tree(positions):
        # continue

        grid = [[0] * max_x for _ in range(max_y)]
        for robot in robots:
            grid[robot.position.y][robot.position.x] = 1
        plt.imshow(grid)
        plt.title(f"Step {t}")
        plt.show()
