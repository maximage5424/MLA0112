from collections import defaultdict, deque

graph = defaultdict(list)

# Undirected graph
edges = [(1,2), (1,3), (1,4), (2,5), (2,6), (3,4), (3,7), (4,8), (7,8)]
for u, v in edges:
    graph[u].append(v)
    graph[v].append(u)  # undirected!

def bfs(start):
    visited = set()
    queue = deque([start])
    visited.add(start)
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return order

def dfs(start, visited=None, order=None):
    if visited is None:
        visited = set()
        order = []
    visited.add(start)
    order.append(start)
    for neighbor in graph[start]:
        if neighbor not in visited:
            dfs(neighbor, visited, order)
    return order

print("BFS from node 1:", bfs(1))
print("DFS from node 1:", dfs(1))