"""
Depth-Limited Search (DLS)
---------------------------
Tree from the notebook:
         A          ← Level 0
        / \
       B   C        ← Level 1
      / \ / \
     D  E F         ← Level 2
    /\ /  \
   G H I   O        ← Level 3

Limitation (depth limit) = 2  →  only explores down to Level 2
"""

from collections import defaultdict

# ──────────────────────────────────────────────
# 1.  Build the tree exactly as drawn
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
# 2.  Recursive Depth-Limited Search
# ──────────────────────────────────────────────
def depth_limited_search(node, goal, limit, depth=0, path=None, visited=None):
    if path    is None: path    = []
    if visited is None: visited = set()

    path    = path + [node]
    visited.add(node)

    indent = "  " * depth
    print(f"{indent}Visiting: {node}  (depth={depth})")

    # ── Goal check ──
    if node == goal:
        print(f"\n✅  Goal '{goal}' FOUND!  Path: {' → '.join(path)}")
        return path

    # ── Depth limit reached ──
    if depth >= limit:
        print(f"{indent}  ⛔ Depth limit {limit} reached at '{node}'. Cutting off.")
        return None

    # ── Recurse into children ──
    for child in graph.get(node, []):
        if child not in visited:
            result = depth_limited_search(child, goal, limit, depth + 1, path, visited)
            if result is not None:
                return result

    return None   # not found in this branch


# ──────────────────────────────────────────────
# 3.  Main
# ──────────────────────────────────────────────
if __name__ == "__main__":
    start = 'A'
    goal  = 'O'          # change to any node to test
    limit = 2            # depth limit from notebook

    print("=" * 50)
    print("DEPTH-LIMITED SEARCH")
    print(f"  Start : {start}")
    print(f"  Goal  : {goal}")
    print(f"  Limit : {limit}")
    print("=" * 50)

    result = depth_limited_search(start, goal, limit)

    print("=" * 50)
    if result:
        print(f"Path found : {' → '.join(result)}")
    else:
        print(f"❌  '{goal}' NOT found within depth limit {limit}.")
    print("=" * 50)

    # ── Extra: try different limits ──
    print("\n--- Testing different depth limits ---")
    for lim in [1, 2, 3]:
        print(f"\nLimit = {lim}:")
        r = depth_limited_search(start, goal, lim)
        if not r:
            print(f"  Not found within depth {lim}.")
