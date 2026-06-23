"""
Informed Search  –  A* & Greedy Best-First Search
====================================================
Graph from notebook (10/6/26):

  Nodes and heuristic h(n)  (estimated cost to goal G):
    S  : h = 11.5    (start)
    A  : h = 10.1
    D  : h = 9.2
    E  : h = 7.1
    B  : h = 5.8
    F  : h = 3.5
    C  : h = 3.4
    G  : h = 0       (goal)

  Edges (undirected) with costs:
    S → A : 3
    S → D : 4
    A → D : 5
    A → B : 4
    D → E : 2        (reading "9.2 → 7.1" path, edge ≈ 2)
    E → F : 4
    B → C : 4
    F → G : 3.5
    C → G : 3.4      (C is directly connected to G with cost ≈ 3.4)

Formula used:
  Greedy BFS : f(n) = h(n)               (only heuristic)
  A*         : f(n) = g(n) + h(n)        (cost so far + heuristic)
"""

import heapq

# ──────────────────────────────────────────────
# 1.  Graph definition
# ──────────────────────────────────────────────
# edges: { node: [(neighbour, edge_cost), ...] }
graph = {
    'S': [('A', 3),  ('D', 4)],
    'A': [('S', 3),  ('D', 5),  ('B', 4)],
    'D': [('S', 4),  ('A', 5),  ('E', 2)],
    'E': [('D', 2),  ('F', 4)],
    'B': [('A', 4),  ('C', 4)],
    'F': [('E', 4),  ('G', 3.5)],
    'C': [('B', 4),  ('G', 3.4)],
    'G': [('F', 3.5),('C', 3.4)],
}

# heuristic h(n) – straight-line / estimated cost to goal
heuristic = {
    'S': 11.5,
    'A': 10.1,
    'D': 9.2,
    'E': 7.1,
    'B': 5.8,
    'F': 3.5,
    'C': 3.4,
    'G': 0,
}


# ──────────────────────────────────────────────
# 2.  Greedy Best-First Search   f(n) = h(n)
# ──────────────────────────────────────────────
def greedy_best_first(start, goal):
    print("=" * 55)
    print("GREEDY BEST-FIRST SEARCH   f(n) = h(n)")
    print(f"  Start: {start}   Goal: {goal}")
    print("=" * 55)

    # priority queue: (h(n), node, path)
    pq = [(heuristic[start], start, [start])]
    visited = set()

    while pq:
        h, node, path = heapq.heappop(pq)

        if node in visited:
            continue
        visited.add(node)

        print(f"  Visiting: {node}   h={h}")

        if node == goal:
            print(f"\n✅  Goal '{goal}' FOUND!")
            print(f"  Path : {' → '.join(path)}")
            total = sum(
                next(c for n, c in graph[path[i]] if n == path[i+1])
                for i in range(len(path)-1)
            )
            print(f"  Total cost (g) : {total}")
            print("=" * 55)
            return path

        for neighbour, cost in graph.get(node, []):
            if neighbour not in visited:
                heapq.heappush(pq, (heuristic[neighbour], neighbour, path + [neighbour]))

    print("❌  Goal not found.")
    print("=" * 55)
    return None


# ──────────────────────────────────────────────
# 3.  A* Search   f(n) = g(n) + h(n)
# ──────────────────────────────────────────────
def astar(start, goal):
    print("=" * 55)
    print("A* SEARCH   f(n) = g(n) + h(n)")
    print(f"  Start: {start}   Goal: {goal}")
    print("=" * 55)

    # priority queue: (f, g, node, path)
    pq = [(heuristic[start], 0, start, [start])]
    visited = {}   # node → best g seen

    while pq:
        f, g, node, path = heapq.heappop(pq)

        if node in visited and visited[node] <= g:
            continue
        visited[node] = g

        print(f"  Visiting: {node}   g={g:.1f}  h={heuristic[node]}  f={f:.1f}")

        if node == goal:
            print(f"\n✅  Goal '{goal}' FOUND!")
            print(f"  Path        : {' → '.join(path)}")
            print(f"  Total cost  : {g:.1f}")
            print("=" * 55)
            return path

        for neighbour, edge_cost in graph.get(node, []):
            new_g = g + edge_cost
            new_h = heuristic[neighbour]
            new_f = new_g + new_h
            if neighbour not in visited or visited[neighbour] > new_g:
                heapq.heappush(pq, (new_f, new_g, neighbour, path + [neighbour]))

    print("❌  Goal not found.")
    print("=" * 55)
    return None


# ──────────────────────────────────────────────
# 4.  Main
# ──────────────────────────────────────────────
if __name__ == "__main__":
    START = 'S'
    GOAL  = 'G'

    print("\n📌  Heuristic table (h values from notebook):")
    for node, h in heuristic.items():
        print(f"    {node} : {h}")

    print()
    greedy_best_first(START, GOAL)

    print()
    astar(START, GOAL)
