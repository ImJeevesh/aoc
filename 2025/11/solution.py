from collections import defaultdict, deque


def parse(input_file):
    with open(input_file) as f:
        lines = f.readlines()

    adj = defaultdict(list)
    in_degree = defaultdict(int)
    all_nodes = set()

    for line in lines:
        if not line.strip():
            continue

        parts = line.strip().split(": ")
        u = parts[0]
        all_nodes.add(u)

        if len(parts) > 1:
            neighbors = parts[1].split()

            for v in neighbors:
                adj[u].append(v)
                in_degree[v] += 1
                all_nodes.add(v)

    for node in all_nodes:
        if node not in in_degree:
            in_degree[node] = 0

    sorted_nodes = []
    queue = deque([u for u in all_nodes if in_degree[u] == 0])
    current_in_degree = in_degree.copy()

    while queue:
        u = queue.popleft()
        sorted_nodes.append(u)

        if u in adj:
            for v in adj[u]:
                current_in_degree[v] -= 1
                if current_in_degree[v] == 0:
                    queue.append(v)

    return sorted_nodes, all_nodes, adj


def solution(input_file):
    sorted_nodes, all_nodes, adj = parse(input_file)

    def paths_base(start, end):
        if start not in all_nodes or end not in all_nodes:
            return 0

        ways = defaultdict(int)
        ways[start] = 1

        for u in sorted_nodes:
            if ways[u] == 0:
                continue

            if u == end:
                return ways[u]

            if u in adj:
                for v in adj[u]:
                    ways[v] += ways[u]

        return ways[end]

    def paths(*order):
        ways = 1
        for i in range(len(order) - 1):
            ways *= paths_base(order[i], order[i + 1])
        return ways

    you_out = paths_base("you", "out")
    svr_out = paths("svr", "dac", "fft", "out") + paths("svr", "fft", "dac", "out")

    return you_out, svr_out
