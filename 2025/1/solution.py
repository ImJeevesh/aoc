def map_rotation(r):
    return -1 if r[0] == "L" else 1, int(r[1:])


def parse_rotations(input_file):
    with open(input_file) as f:
        rotations = f.read().splitlines()
    return [map_rotation(r) for r in rotations]


def solution(input_file):
    hits, crosses = 0, 0
    size, start = 100, 50

    rotations = parse_rotations(input_file)
    dial = start

    for direction, clicks in rotations:
        if direction < 0:
            target = dial or size
        else:
            target = size - dial

        dial = (dial + direction * clicks) % size

        if dial == 0:
            hits += 1

        if clicks >= target:
            crosses += (clicks - target) // size + 1

    return hits, crosses
