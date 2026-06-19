graph = {
    'P': ['R', 'C', 'A'],
    'A': ['M_a'],
    'C': ['R', 'U', 'M_a'],
    'R': ['E'],
    'E': ['S', 'U'],
    'U': ['S', 'M_b'],
    'M_a': ['U', 'L_a'],
    'L_a': ['M_b'],
    'M_b': ['S'],
    'S': []
}

heuristic = {
    'P': 10, 'A': 11, 'R': 8, 'C': 8,
    'E': 3, 'M_a': 8, 'U': 4, 'S': 10,
    'L_a': 9, 'M_b': 9
}

def greedy_best_first(start, goal):
    path = [start]
    current = start

    while current != goal:
        neighbors = graph.get(current, [])
        if not neighbors:
            break
        next_node = min(neighbors, key=lambda n: heuristic[n])
        path.append(next_node)
        current = next_node

    return path

path = greedy_best_first('P', 'S')
print("Path:", " -> ".join(path))