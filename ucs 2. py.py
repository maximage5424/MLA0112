import heapq

graph = {
    'S': [('A', 3), ('B', 2), ('C', 7)],
    'A': [('D', 3), ('E', 8), ('G', 15)],
    'B': [('G', 20)],
    'C': [('G', 6)],   # corrected from 9 to 6
    'D': [],
    'E': [],
    'G': []
}

def ucs(start, goal):
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