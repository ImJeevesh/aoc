from itertools import combinations


def parse_positions(input_file):
    with open(input_file) as f:
        return [tuple(map(int, line.strip().split(","))) for line in f]


def minmax(c0, c1):
    return min(c0[0], c1[0]), min(c0[1], c1[1]), max(c0[0], c1[0]), max(c0[1], c1[1])


def is_inside(rect, positions):
    min_x, min_y, max_x, max_y = minmax(*rect)

    n = len(positions)

    for px, py in positions:
        if min_x < px < max_x and min_y < py < max_y:
            return False

    for i in range(n):
        current = positions[i]
        next = positions[(i + 1) % n]

        if current[0] == next[0]:
            ex = current[0]
            _, ey_min, _, ey_max = minmax(current, next)

            if min_x < ex < max_x and ey_min <= min_y and ey_max >= max_y:
                return False
        else:
            ey = current[1]
            ex_min, _, ex_max, _ = minmax(current, next)

            if min_y < ey < max_y and ex_min <= min_x and ex_max >= max_x:
                return False

    mx = (min_x + max_x) / 2
    my = (min_y + max_y) / 2
    intersections = 0

    for i in range(n):
        u, v = positions[i], positions[(i + 1) % n]

        if u[0] == v[0]:
            ex = u[0]
            _, ey_min, _, ey_max = minmax(u, v)

            if ex > mx:
                if (ey_min > my) != (ey_max > my):
                    intersections += 1

    if intersections % 2 == 0:
        return False

    return True


def solution(input_file):
    positions = parse_positions(input_file)

    rects = []
    for c0, c1 in combinations(positions, 2):
        x0, y0 = c0
        x1, y1 = c1
        width = abs(x0 - x1) + 1
        height = abs(y0 - y1) + 1
        area = width * height
        rects.append((area, c0, c1))

    rects.sort(key=lambda x: x[0], reverse=True)

    max_area_p1 = rects[0][0]
    max_area_p2 = 0

    for area, c0, c1 in rects:
        if is_inside((c0, c1), positions):
            max_area_p2 = area
            break

    return max_area_p1, max_area_p2
