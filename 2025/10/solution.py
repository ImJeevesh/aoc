from itertools import combinations


def parse_machine(line):
    left, *mid, right = line.split()
    lights = {i for i, c in enumerate(left.strip("[]")) if c == "#"}
    buttons = [set(map(int, p.strip("()").split(","))) for p in mid]
    joltages = list(map(int, right.strip("{}").split(",")))
    return lights, buttons, joltages


def solve_indicator_lights(buttons, target):
    for p in range(1, len(buttons) + 1):
        for combo in combinations(buttons, p):
            current = set()

            for b in combo:
                current ^= b

            if current == target:
                return p
    return 0


def gaussian_elimination(matrix):
    nc = len(matrix[0])
    cr = 0
    fvars = []

    for col in range(nc - 1):
        pr = next((i for i in range(cr, len(matrix)) if matrix[i][col]), None)

        if pr is None:
            fvars.append(col)
            continue

        matrix[cr], matrix[pr] = matrix[pr], matrix[cr]

        for r, row in enumerate(matrix):
            if r == cr:
                continue

            coefficient = row[col]
            for c in range(nc):
                row[c] = row[c] * matrix[cr][col] - matrix[cr][c] * coefficient

        cr += 1

    return matrix, fvars


def calculate_variable_bounds(fvars, buttons, joltages):
    bounds = []

    for fv in fvars:
        vj = [joltages[i] for i in buttons[fv] if i < len(joltages)]
        bounds.append(min(vj) if vj else 0)

    return bounds


def solve_joltage_counters(buttons, joltages):
    matrix = [[0] * (len(buttons) + 1) for _ in range(len(joltages))]

    for i, btn in enumerate(buttons):
        for j in btn:
            matrix[j][i] = 1

    for i, joltage in enumerate(joltages):
        matrix[i][-1] = joltage

    matrix, fvars = gaussian_elimination(matrix)

    bounds = calculate_variable_bounds(fvars, buttons, joltages)

    assignment = [0] * len(fvars)
    min_p = float("inf")

    def search(v_idx, current_total):
        nonlocal min_p

        if current_total >= min_p:
            return

        if v_idx == len(fvars):
            total = current_total

            for row in matrix:
                pivot = next((v for v in row if v), 0)
                if not pivot:
                    continue

                rhs = row[-1]
                for i, v in zip(fvars, assignment):
                    rhs -= row[i] * v

                q, r = divmod(rhs, pivot)
                if r or q < 0:
                    return

                total += q
                if total >= min_p:
                    return

            if total < min_p:
                min_p = total
            return

        for value in range(bounds[v_idx] + 1):
            assignment[v_idx] = value
            search(v_idx + 1, current_total + value)

    search(0, 0)

    return min_p if min_p != float("inf") else 0


def solution(input_file):
    p1 = 0
    p2 = 0

    with open(input_file) as f:
        for line in f.read().splitlines():
            lights, buttons, joltages = parse_machine(line)
            p1 += solve_indicator_lights(buttons, lights)
            p2 += solve_joltage_counters(buttons, joltages)

    return p1, p2
