graph = {
    'A': ['B', 'C', 'D'],
    'B': ['E'],
    'C': ['F', 'E'],
    'D': ['F'],
    'E': ['H'],
    'F': ['H'],
    'H': ['G'],
    'G': []
}

heuristic = {
    'A': 40, 'B': 32, 'C': 26, 'D': 35,
    'E': 19, 'F': 17, 'H': 10, 'G': 0
}

def greedy_best_first(start, goal):
    path = [start]
    current = start

    while current != goal:
        neighbors = graph.get(current, [])
        if not neighbors:
            break
        # pick neighbor with smallest heuristic value
        next_node = min(neighbors, key=lambda n: heuristic[n])
        path.append(next_node)
        current = next_node

    return path

path = greedy_best_first('A', 'G')
print("Path:", " -> ".join(path))