adjs = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]


def can_forklift_pickup(stacks, r, c):
    rolls = 0

    for orr, occ in adjs:
        dr, dc = r + orr, c + occ

        if dr < 0 or dr >= len(stacks) or dc < 0 or dc >= len(stacks):
            continue

        if stacks[dr][dc] == "@":
            rolls += 1

    return rolls < 4


def run(grid):
    picked = set()
    rows, cols = len(grid), len(grid[0])

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "@":
                if can_forklift_pickup(grid, r, c):
                    picked.add((r, c))

    return picked


def patch_grid(grid, picked):
    for r, c in picked:
        grid[r][c] = "."


def solution(input_file):
    total = 0
    first = None

    with open(input_file) as f:
        grid = [list(line) for line in f.read().splitlines()]

        while True:
            picked = run(grid)
            total += len(picked)
            patch_grid(grid, picked)

            if first is None:
                first = total

            if len(picked) == 0:
                break

    return first, total
