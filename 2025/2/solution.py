def parse_ranges(input_file):
    ranges = []

    with open(input_file) as f:
        line = f.read().strip()
        ranges = line.split(",")

    return [tuple(r.split("-")) for r in ranges]


def is_exactly_twice(id):
    n = len(id)
    mid = n // 2
    return n % 2 == 0 and id[:mid] == id[mid:]


def is_atleast_twice(id):
    if is_exactly_twice(id):
        return True

    n = len(id)
    mid = n // 2

    for digits in range(1, mid + 1):
        if n % digits == 0:
            pattern = id[:digits]

            if pattern * (n // digits) == id:
                return True


def solution(input_file):
    p1 = 0
    p2 = 0

    ranges = parse_ranges(input_file)

    for first, last in ranges:
        for num in range(int(first), int(last) + 1):
            if is_exactly_twice(str(num)):
                p1 += num
                p2 += num
            elif is_atleast_twice(str(num)):
                p2 += num

    return p1, p2
