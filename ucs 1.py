import heapq

graph = {
    'S': [('A', 1), ('G', 12)],
    'A': [('B', 3), ('C', 1)],
    'B': [('D', 3)],
    'C': [('D', 1), ('G', 2)],
    'D': [('G', 3)],
    'G': [('D', 3), ('C', 2)]
}

def ucs(start, goal):
    # priority queue: (cost, node, path)
    queue = [(0, start, [start])]
    visited = set()

    while queue:
        cost, node, path = heapq.heappop(queue)

        if node == goal:
            return cost, path

        if node in visited:
            continue
        visited.add(node)

        for neighbor, weight in graph.get(node, []):
            if neighbor not in visited:
                heapq.heappush(queue, (cost + weight, neighbor, path + [neighbor]))

    return float('inf'), []

cost, path = ucs('S', 'G')
print("Minimum cost:", cost)
print("Path:", " -> ".join(path))