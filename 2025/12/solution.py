import sys
from collections import Counter
from utils import run_parallel

sys.setrecursionlimit(5000)


class Shape:
    def __init__(self, id, grid):
        self.id = id
        self.grid = grid
        self.variations = self._generate_variations()

    def _generate_variations(self):
        variations = []
        current = self.grid

        for _ in range(2):
            for _ in range(4):
                coords = self._grid_to_coords(current)

                if coords:
                    variations.append(coords)

                current = self._rotate(current)
            current = self._flip(current)

        unique_vars = []
        seen = set()

        for v in variations:
            v_tuple = tuple(sorted(v))

            if v_tuple not in seen:
                seen.add(v_tuple)
                unique_vars.append(v)

        return unique_vars

    def _grid_to_coords(self, grid):
        coords = []
        if not grid:
            return coords

        rows = len(grid)
        cols = len(grid[0])

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == "#":
                    coords.append((r, c))

        if not coords:
            return coords

        min_r = min(r for r, c in coords)
        min_c = min(c for r, c in coords)

        return [(r - min_r, c - min_c) for r, c in coords]

    def _rotate(self, grid):
        return [list(row) for row in zip(*grid[::-1])]

    def _flip(self, grid):
        return [row[::-1] for row in grid]


def parse_input(input_file):
    with open(input_file, "r") as f:
        content = f.read()

    shapes = {}
    regions = []

    lines = content.splitlines()
    blocks = content.strip().split("\n\n")

    for block in blocks:
        lines = block.strip().splitlines()
        header = lines[0]

        if ":" in header:
            pre_colon = header.split(":")[0]

            if "x" in pre_colon:
                for line in lines:
                    parts = line.split(":")
                    dims = parts[0].split("x")
                    w, h = int(dims[0]), int(dims[1])
                    counts = list(map(int, parts[1].strip().split()))
                    regions.append({"w": w, "h": h, "counts": counts})
            else:
                shape_id = int(pre_colon)
                grid = [list(line_str) for line_str in lines[1:]]
                shapes[shape_id] = Shape(shape_id, grid)

    return shapes, regions


def quick_solve_region(region, n):
    w, h = region["w"], region["h"]
    counts = region["counts"]

    if sum(counts) <= (w // n) * (h // n):
        return True


def solve_region(region, shapes):
    w, h = region["w"], region["h"]
    counts = region["counts"]

    to_place_ids = []

    for s_id, count in enumerate(counts):
        for _ in range(count):
            to_place_ids.append(s_id)

    total_area = 0
    needed_ids = set()

    for s_id in to_place_ids:
        s = shapes[s_id]
        variation = s.variations[0]  # base
        area = len(variation)
        total_area += area
        needed_ids.add(s_id)

    area_to_fill = w * h
    if total_area > area_to_fill:
        return False

    num_holes = area_to_fill - total_area

    placements_by_min_bit = {}

    for s_id in needed_ids:
        s = shapes[s_id]
        by_bit = {}

        for var_coords in s.variations:
            v_h = max(r for r, c in var_coords) + 1
            v_w = max(c for r, c in var_coords) + 1

            for tr in range(h - v_h + 1):
                for tc in range(w - v_w + 1):
                    mask = 0
                    min_bit = None

                    for r, c in var_coords:
                        bit = (tr + r) * w + (tc + c)
                        mask |= 1 << bit

                        if min_bit is None or bit < min_bit:
                            min_bit = bit

                    if min_bit not in by_bit:
                        by_bit[min_bit] = []

                    by_bit[min_bit].append(mask)

        placements_by_min_bit[s_id] = by_bit

    req_counts = Counter(to_place_ids)

    sorted_shape_ids = sorted(
        list(needed_ids), key=lambda sid: -len(shapes[sid].variations[0])
    )

    full_mask = (1 << (w * h)) - 1

    def backtrack(board_mask, current_counts, holes_left):
        if board_mask == full_mask:
            return True

        low_bit_val = (~board_mask) & (board_mask + 1)
        first_empty_idx = low_bit_val.bit_length() - 1

        for s_id in sorted_shape_ids:
            if current_counts[s_id] > 0:
                if (
                    s_id in placements_by_min_bit
                    and first_empty_idx in placements_by_min_bit[s_id]
                ):
                    for p_mask in placements_by_min_bit[s_id][first_empty_idx]:
                        if (board_mask & p_mask) == 0:
                            current_counts[s_id] -= 1
                            if backtrack(
                                board_mask | p_mask, current_counts, holes_left
                            ):
                                return True
                            current_counts[s_id] += 1

        if holes_left > 0:
            if backtrack(board_mask | low_bit_val, current_counts, holes_left - 1):
                return True

        return False

    return backtrack(0, req_counts, num_holes)


def worker(args):
    region, shapes = args
    return solve_region(region, shapes)


def solution(input_file, alt=False):
    shapes, regions = parse_input(input_file)

    valid_count = 0

    if alt:
        tasks = [(r, shapes) for r in regions]
        results = run_parallel(worker, tasks)

        for is_valid in results:
            if is_valid:
                valid_count += 1

        return valid_count

    for region in regions:
        if quick_solve_region(region, len(shapes)):
            valid_count += 1

    return valid_count
