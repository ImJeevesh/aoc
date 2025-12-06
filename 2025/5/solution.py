def parse_input(input_file):
    fresh_ranges, available = [], []

    with open(input_file) as f:
        for line in f:
            if line.strip() == "":
                break

            fresh_ranges.append(tuple(map(int, line.strip().split("-"))))

        for line in f:
            available.append(int(line.strip()))

    return sorted(fresh_ranges), sorted(available)


def get_fresh_total(fresh_ranges):
    fresh_total = 0
    current = -1
    for f, b in fresh_ranges:
        if current >= f:
            f = current + 1

        if f <= b:
            fresh_total += b - f + 1

        current = max(current, b)

    return fresh_total


def solution(input_file):
    fresh_ranges, available = parse_input(input_file)

    fresh_total = get_fresh_total(fresh_ranges)
    fresh_count = 0
    for ingredient in available:
        for f, b in fresh_ranges:
            if ingredient >= f and ingredient <= b:
                fresh_count += 1
                break

    return fresh_count, fresh_total
