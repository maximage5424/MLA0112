import heapq

graph = {
    'A': [('B', 1), ('C', 4)],
    'B': [('C', 2), ('D', 3)],
    'C': [('E', 5)],
    'D': [('F', 2), ('G', 4)],
    'E': [('G', 3)],
    'F': [('G', 1)],
    'G': []
}

heuristic = {
    'A': 5, 'B': 6, 'C': 4, 'D': 3,
    'E': 3, 'F': 1, 'G': 0
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

cost, path = astar('A', 'G')
print("Total cost:", cost)
print("Path:", " -> ".join(path))