import argparse
import importlib.util
import io
import os
from typing import Callable


def get_solver(day_folder, part: int) -> Callable[[io.StringIO], int]:
    # Get the spec
    spec = importlib.util.spec_from_file_location(
        "solution", os.path.join(day_folder, "solution.py")
    )

    # Create the module
    module = importlib.util.module_from_spec(spec)  # type: ignore

    # Execute the module
    spec.loader.exec_module(module)  # type: ignore

    if part == 1:
        return module.get_answer_to_part_1
    if part == 2:
        return module.get_answer_to_part_2
    raise ValueError(f"Invalid part {part}")


def main(year: int, day: int, test: bool, part: int):
    day_folder = f"year{year}\\day{day}"
    if test:
        input_file = "test_input.txt"
    else:
        input_file = "real_input.txt"

    file = open(os.path.join(day_folder, input_file), "r")

    solver = get_solver(day_folder, part)
    solution = solver(file)  # type: ignore
    print(f"Solution to day {day} part {part} ({test = }): {solution}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("year", type=int)
    parser.add_argument("day", type=int)
    parser.add_argument("test", type=int)
    parser.add_argument("part", type=int)
    args = parser.parse_args()
    main(args.year, args.day, bool(args.test), args.part)
