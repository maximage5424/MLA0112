import heapq

graph = {
    'S': [('A', 3), ('D', 2)],
    'A': [('B', 5)],
    'B': [('C', 2), ('D', 1), ('E', 1)],
    'D': [('E', 4)],
    'C': [('G', 4)],
    'E': [('G', 3)],
    'G': []
}

heuristic = {
    'S': 7, 'A': 9, 'B': 4, 'C': 2,
    'D': 5, 'E': 3, 'G': 0
}

def astar(start, goal):
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