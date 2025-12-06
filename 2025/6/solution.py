from math import prod


def parse_grid(input_file, row_parser):
    with open(input_file) as f:
        lines = f.readlines()
    grid = [row_parser(line) for line in lines]
    operators = grid.pop()
    return grid, operators


def part_1(input_file):
    grid, operators = parse_grid(input_file, lambda line: line.split())

    total = 0
    for col_idx, op in enumerate(operators):
        values = [int(row[col_idx]) for row in grid]
        if op == "*":
            total += prod(values)
        elif op == "+":
            total += sum(values)

    return total


def part_2(input_file):
    grid, operators = parse_grid(input_file, list)

    col_totals = []
    values = []

    for col_idx in range(len(operators) - 1, -1, -1):
        col_str = "".join(row[col_idx] for row in grid).strip()

        if not col_str:
            continue

        values.append(int(col_str))
        op = operators[col_idx]

        if op == "*":
            col_totals.append(prod(values))
            values = []
        elif op == "+":
            col_totals.append(sum(values))
            values = []

    return sum(col_totals)


def solution(input_file):
    return part_1(input_file), part_2(input_file)
