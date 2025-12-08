from utils.union_find import UnionFind
from itertools import combinations


def parse_coordinates(input_file):
    with open(input_file) as f:
        return [tuple(map(int, line.strip().split(","))) for line in f]


def dist_sq(p1, p2):
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    return (x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2


def get_pairs(coordinates, sort_by_dist=False):
    n = len(coordinates)
    pairs = []

    for i, j in combinations(range(n), 2):
        d = dist_sq(coordinates[i], coordinates[j])
        pairs.append((d, i, j))

    if sort_by_dist:
        pairs.sort(key=lambda x: x[0])

    return pairs


def part_one(input_file):
    coordinates = parse_coordinates(input_file)
    n = len(coordinates)

    pairs = get_pairs(coordinates)

    uf = UnionFind(n)

    for pair_idx in range(len(pairs)):
        _, i, j = pairs[pair_idx]
        uf.union(i, j)

    sizes = []
    for i in range(n):
        if uf.parent[i] == i:
            sizes.append(uf.size[i])

    sizes.sort(reverse=True)

    result = 1
    for s in sizes[:3]:
        result *= s

    return result


def part_two(input_file):
    coordinates = parse_coordinates(input_file)
    n = len(coordinates)

    pairs = get_pairs(coordinates, sort_by_dist=True)

    uf = UnionFind(n)

    components_count = n

    for d, i, j in pairs:
        if uf.union(i, j):
            components_count -= 1
            if components_count == 1:
                p1 = coordinates[i]
                p2 = coordinates[j]
                return p1[0] * p2[0]


def solution(input_file):
    return part_one(input_file), part_two(input_file)
