from pathlib import Path
from datetime import datetime
from argparse import ArgumentParser
import importlib.util
import sys
import time


def get_arguments():
    parser = ArgumentParser(description="Advent of Code - 2025")
    parser.add_argument(
        "-y",
        "--year",
        type=int,
        default=datetime.now().year,
        help="select year (default: current year)",
    )
    parser.add_argument(
        "-d",
        "--day",
        type=int,
        default=datetime.now().day,
        help="select day (default: current day)",
    )
    parser.add_argument(
        "-c",
        "--create",
        action="store_true",
        help="create day directory",
    )
    parser.add_argument(
        "-e",
        "--example",
        action="store_true",
        help="run (example)",
    )
    parser.add_argument(
        "-i",
        "--input",
        action="store_true",
        help="run (input)",
    )

    args = parser.parse_args()
    if args.example is False and args.input is False:
        args.example = True
        args.input = True

    return args


def create_day(year: int, day: int):
    day_path = Path(str(year)) / str(day)

    print(f"aoc: create {year} / {day}")

    if day_path.exists():
        print(f"aoc: {year} / {day} already exists")
        return

    day_path.mkdir(parents=True, exist_ok=True)
    (day_path / "example.txt").write_text("")
    (day_path / "input.txt").write_text("")
    (day_path / "solution.py").write_text("def solution(input_file):\n    return 0")


def run_func(func, input_file):
    start_time = time.time()
    result = func(str(input_file))
    end_time = time.time()
    return result, end_time - start_time


def run_day(year: int, day: int, run_example: bool, run_input: bool):
    day_path = Path(str(year)) / str(day)
    solution_path = day_path / "solution.py"
    input_file = day_path / "input.txt"
    example_file = day_path / "example.txt"

    if not solution_path.exists():
        print(f"aoc: {year} / {day} not found. Run with -c/--create to create it.")
        return

    spec = importlib.util.spec_from_file_location(f"day_{day}_solution", solution_path)
    if spec is None or spec.loader is None:
        print(f"aoc: failed to load solution from {solution_path}")
        return

    module = importlib.util.module_from_spec(spec)
    sys.modules[f"day_{day}_solution"] = module
    spec.loader.exec_module(module)

    print(f"aoc: {year} / {day}\n")

    tasks = []
    if run_example:
        if not example_file.exists():
            print(f"aoc: {year} / {day} example file not found: {example_file}")
        else:
            tasks.append(("example", example_file))

        # optional
        example_file_alt = day_path / "example-alt.txt"
        if example_file_alt.exists():
            tasks.append(("example - alt", example_file_alt))

    if run_input:
        if not input_file.exists():
            print(f"aoc: {year} / {day} input file not found: {input_file}")
        else:
            tasks.append(("input", input_file))

    for label, file_path in tasks:
        print(f"--- {label} ---")
        if hasattr(module, "solution"):
            res, duration = run_func(module.solution, file_path)
            print(f"result: {res}")
            print(f"time: {duration:.4f}s\n")
        else:
            print(f"error: 'solution' function not found in {solution_path}")


def main(args):
    if args.create:
        create_day(args.year, args.day)
    else:
        run_day(args.year, args.day, args.example, args.input)


if __name__ == "__main__":
    main(get_arguments())
