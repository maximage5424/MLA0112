import heapq

graph = {
    'S': [('A', 3), ('D', 4)],
    'A': [('B', 4), ('D', 5)],
    'B': [('C', 4), ('E', 5)],
    'D': [('E', 2)],
    'E': [('F', 4)],
    'F': [('G', 3.5)],
    'C': [],
    'G': []
}

heuristic = {
    'S': 11.5, 'A': 10.1, 'B': 8.8, 'C': 3.1,
    'D': 9.2, 'E': 7.1, 'F': 3.5, 'G': 0
}

def astar(start, goal):
    # (f, g, node, path)
    queue = [(heuristic[start], 0, start, [start])]
    visited = set()

    while queue:
        f, g, node, path = heapq.heappop(queue)

        if node == goal:
            return g, path

        if node in visited:
            continue
        visited.add(node)

        for neighbor, cost in graph.get(node, []):
            if neighbor not in visited:
                new_g = g + cost
                new_f = new_g + heuristic[neighbor]
                heapq.heappush(queue, (new_f, new_g, neighbor, path + [neighbor]))

    return float('inf'), []

cost, path = astar('S', 'G')
print("Total cost:", cost)
print("Path:", " -> ".join(path))