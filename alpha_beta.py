"""
Alpha-Beta Pruning  (Image 2)
==============================
Tree from notebook:
         A (MAX)
        / \
       B   C (MIN)
      /|    |\
     D E    F  G (MAX)
    /| |    |  |\
   H  I J  K  L  M N O (terminal)
   Leaf values (left to right): 1, 2, 5, 1, 0, -6, 4

Levels: MAX → MIN → MAX → MIN (terminal leaves)

"We are removing unwanted nodes when the
 minimum/maximum value is noticed."
"""

import math

# ──────────────────────────────────────────────
# 1.  Tree definition
#     Each node: { 'children': [...] } or leaf value
# ──────────────────────────────────────────────
# Terminal leaf values (left-to-right): 1, 2, 5, 1, 0, -6, 4
# Build tree bottom-up matching the notebook diagram

tree = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F', 'G'],
    'D': ['H', 'I'],
    'E': ['J'],
    'F': ['K'],
    'G': ['L', 'M'],
    # terminal nodes → values
    'H': 1,
    'I': 2,
    'J': 5,
    'K': 1,
    'L': 0,
    'M': -6,
    # Extra leaf from notebook: 4
    # (attached to N if present, otherwise treat as extra child of G)
}

# Alternative cleaner representation as nested lists:
# (MAX, (MIN, (MAX, 1, 2), (MAX, 5)), (MIN, (MAX, 1), (MAX, 0, -6, 4)))

# We'll use the nested-list form for a clean implementation:
#   Each node is either an int (leaf) or (is_max: bool, *children)

TREE = (True,                          # A – MAX
    (False,                            # B – MIN
        (True, 1, 2),                  # D – MAX  → leaves 1, 2
        (True, 5),                     # E – MAX  → leaf  5
    ),
    (False,                            # C – MIN
        (True, 1),                     # F – MAX  → leaf  1
        (True, 0, -6, 4),              # G – MAX  → leaves 0, -6, 4
    ),
)

pruned_nodes = []   # track pruned nodes

# ──────────────────────────────────────────────
# 2.  Alpha-Beta
# ──────────────────────────────────────────────
def alpha_beta(node, alpha, beta, depth=0):
    indent = "  " * depth

    # Leaf node
    if isinstance(node, int):
        print(f"{indent}Leaf  value = {node}")
        return node

    is_max = node[0]
    children = node[1:]
    node_type = "MAX" if is_max else "MIN"
    print(f"{indent}[{node_type}]  α={alpha}  β={beta}")

    if is_max:
        value = -math.inf
        for child in children:
            child_val = alpha_beta(child, alpha, beta, depth + 1)
            value = max(value, child_val)
            alpha = max(alpha, value)
            print(f"{indent}  → updated α={alpha}  current best={value}")
            if alpha >= beta:
                print(f"{indent}  ✂️  PRUNED (β cut-off)  α={alpha} ≥ β={beta}")
                pruned_nodes.append(f"remaining siblings at depth {depth+1}")
                break
        return value
    else:
        value = math.inf
        for child in children:
            child_val = alpha_beta(child, alpha, beta, depth + 1)
            value = min(value, child_val)
            beta = min(beta, value)
            print(f"{indent}  → updated β={beta}  current best={value}")
            if alpha >= beta:
                print(f"{indent}  ✂️  PRUNED (α cut-off)  α={alpha} ≥ β={beta}")
                pruned_nodes.append(f"remaining siblings at depth {depth+1}")
                break
        return value

# ──────────────────────────────────────────────
# 3.  Main
# ──────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print("ALPHA-BETA PRUNING")
    print("  MAX levels: A, D, E, F, G")
    print("  MIN levels: B, C")
    print("=" * 55)

    result = alpha_beta(TREE, -math.inf, math.inf)

    print("=" * 55)
    print(f"✅  Optimal value at root (A) = {result}")
    print(f"   Prunings occurred : {len(pruned_nodes)}")
    print("=" * 55)
