"""
Iterative Deepening Search (IDS)
----------------------------------
From the notebook:
  I0 = A                      (depth limit 0)
  I1 = B → C                  (depth limit 1)
  I2 = D → E → F → G          (depth limit 2)

Note: "When the right-side node is the goal node,
       we can use iterative deepening."

Tree used (same as DLS notebook page):
         A          ← Level 0
        / \
       B   C        ← Level 1
      / \   \
     D   E   F      ← Level 2
    /\   |    \
   G  H  I     O   ← Level 3
"""

# ──────────────────────────────────────────────
# 1.  Graph (tree) definition
# ──────────────────────────────────────────────
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': ['G', 'H'],
    'E': ['I'],
    'F': ['O'],
    'G': [],
    'H': [],
    'I': [],
    'O': [],
}

# ──────────────────────────────────────────────
# 2.  Depth-Limited DFS (helper for IDS)
# ──────────────────────────────────────────────
def dls(node, goal, limit, depth=0, path=None):
    if path is None:
        path = []
    path = path + [node]

    if node == goal:
        return path              # 🎯 found

    if depth >= limit:
        return None              # cut-off

    for child in graph.get(node, []):
        result = dls(child, goal, limit, depth + 1, path)
        if result is not None:
            return result

    return None


# ──────────────────────────────────────────────
# 3.  Iterative Deepening Search
# ──────────────────────────────────────────────
def iterative_deepening_search(start, goal, max_depth=10):
    print("=" * 55)
    print("ITERATIVE DEEPENING SEARCH (IDS)")
    print(f"  Start : {start}   Goal : {goal}")
    print("=" * 55)

    for depth_limit in range(max_depth + 1):
        print(f"\n[Iteration I{depth_limit}]  depth_limit = {depth_limit}")

        # collect nodes visited at this iteration for display
        visited_order = []
        _dls_verbose(start, goal, depth_limit, 0, [], visited_order)
        print(f"  Nodes explored : {' → '.join(visited_order)}")

        result = dls(start, goal, depth_limit)

        if result is not None:
            print(f"\n✅  Goal '{goal}' FOUND at depth limit {depth_limit}!")
            print(f"  Path : {' → '.join(result)}")
            print("=" * 55)
            return result

        print(f"  ❌  Not found within depth {depth_limit}.")

    print("=" * 55)
    print(f"Goal '{goal}' NOT found within max depth {max_depth}.")
    return None


# ──────────────────────────────────────────────
# 4.  Verbose DLS (only for printing visit order)
# ──────────────────────────────────────────────
def _dls_verbose(node, goal, limit, depth, path, visited_order):
    visited_order.append(node)
    if node == goal or depth >= limit:
        return
    for child in graph.get(node, []):
        _dls_verbose(child, goal, limit, depth + 1, path + [node], visited_order)


# ──────────────────────────────────────────────
# 5.  Main
# ──────────────────────────────────────────────
if __name__ == "__main__":
    # ── Test 1: goal = G  (matches notebook: I2 = D→E→F→G) ──
    print("\n📌 Test 1: Find G")
    iterative_deepening_search('A', 'G')

    # ── Test 2: goal = O  (deepest right-side node) ──
    print("\n📌 Test 2: Find O (right-side goal)")
    iterative_deepening_search('A', 'O')

    # ── Test 3: goal = C  (level 1, right side) ──
    print("\n📌 Test 3: Find C")
    iterative_deepening_search('A', 'C')
