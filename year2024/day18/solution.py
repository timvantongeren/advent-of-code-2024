from collections import defaultdict
from dataclasses import dataclass
import io

from tqdm import tqdm


@dataclass(eq=True, frozen=True)
class Location:
    x: int
    y: int

    def __add__(self, other):
        return Location(self.x + other.x, self.y + other.y)


def parse_bytes(lines: list[str]) -> list[Location]:
    return [Location(int(a), int(b)) for a, b in [line.split(",") for line in lines]]


directions = [Location(1, 0), Location(-1, 0), Location(0, 1), Location(0, -1)]


def within_bounds(loc: Location, max_distance: int) -> bool:
    return (0 <= loc.x <= max_distance) and (0 <= loc.y <= max_distance)


def get_next_step_locations(
    location: Location,
    step: int,
    fallen_bytes: set[Location],
    locations_seen: dict[int, set[Location]],
    max_distance: int,
):
    for dir in directions:
        next_location = location + dir
        if any([next_location in locations_seen[i] for i in range(step)]):
            # No point in having a route see the same point later
            continue
        if not within_bounds(next_location, max_distance):
            # can't move there
            continue
        if next_location in fallen_bytes:
            # can't move there
            continue
        # we can actually go here
        locations_seen[step].add(next_location)


def get_answer_to_part_1(input_stream: io.StringIO) -> int:
    lines = input_stream.readlines()
    falling_bytes = parse_bytes(lines)
    fallen_bytes = falling_bytes[:1024]  # change to 1024 for real
    set_of_bytes = set(fallen_bytes)

    max_distance = 70  # set to 70 for real
    target = Location(max_distance, max_distance)

    current_location = Location(0, 0)
    locations_seen_at_step: dict[int, set[Location]] = defaultdict(set)
    locations_seen_at_step[0].add(current_location)

    for step in tqdm(range(1, 10_000)):
        previous_locations = locations_seen_at_step[step - 1]
        for location in previous_locations:
            get_next_step_locations(
                location, step, set_of_bytes, locations_seen_at_step, max_distance
            )
        if target in locations_seen_at_step[step]:
            return step


def path_is_connected(reachable_locations: set[Location]) -> bool:
    if not reachable_locations:
        return False
    return all(
        [any([loc + d in reachable_locations for d in directions]) for loc in reachable_locations]
    )


assert path_is_connected(set([Location(0, 0), Location(0, 1)]))
assert not path_is_connected(set([Location(0, 0), Location(1, 1)]))
assert not path_is_connected(set([]))


def backtrack_path(locations_at_steps: dict[int, set[Location]], last_step: int) -> set[Location]:
    this_step = locations_at_steps[last_step].pop()
    path: set[Location] = set([this_step])
    for step in reversed(range(0, last_step - 1)):
        found = False
        for loc in locations_at_steps[step]:
            for direction in directions:
                if loc + direction == this_step:
                    path.add(loc)
                    this_step = loc
                    found = True
                    break
            if found:
                break
    return path


def get_path(set_of_bytes, max_distance, target, max_steps: int) -> set[Location]:
    current_location = Location(0, 0)
    locations_seen_at_step: dict[int, set[Location]] = defaultdict(set)
    locations_seen_at_step[0].add(current_location)

    for step in range(1, max_steps):
        previous_locations = locations_seen_at_step[step - 1]
        for location in previous_locations:
            get_next_step_locations(
                location, step, set_of_bytes, locations_seen_at_step, max_distance
            )
        if target in locations_seen_at_step[step]:
            return backtrack_path(locations_seen_at_step, step)
    return set()


def get_answer_to_part_2(input_stream: io.StringIO) -> int:
    lines = input_stream.readlines()
    falling_bytes = parse_bytes(lines)
    max_distance = 70  # set to 70 for real
    target = Location(max_distance, max_distance)
    path_found = set()

    for byte_index in tqdm(range(len(falling_bytes))):
        fallen_bytes = falling_bytes[:byte_index]
        set_of_bytes = set(fallen_bytes)
        if path_is_connected(path_found - set_of_bytes):
            # still a working path
            continue
        path_found = get_path(set_of_bytes, max_distance, target, 100_000)
        if not path_found:
            return falling_bytes[byte_index - 1]
