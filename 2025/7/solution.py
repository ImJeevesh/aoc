from collections import defaultdict


def parse_input(input_file):
    with open(input_file) as f:
        return [list(line) for line in f.read().splitlines()]


def solution(input_file):
    grid = parse_input(input_file)
    counts = defaultdict(int)
    start_col = grid[0].index("S")
    counts[start_col] = 1

    splits = 0
    height = len(grid)
    width = len(grid[0])

    for row in range(2, height, 2):
        next_counts = defaultdict(int)
        for col, count in counts.items():
            if col >= width:
                continue

            ch = grid[row][col]
            if ch == "^":
                splits += 1
                if col - 1 >= 0:
                    next_counts[col - 1] += count
                if col + 1 < width:
                    next_counts[col + 1] += count
            else:
                next_counts[col] += count

        counts = next_counts

    return splits, sum(counts.values())
