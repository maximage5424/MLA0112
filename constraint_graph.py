"""
Constraint Graph  (Image 5)
============================
"Make the map's nodes the nodes (of the constraint graph)"

Regions: Chennai, Tirupati, Nellore, Ongole (Arm)
Edges = shared borders (constraints)

This builds and visualizes the constraint graph,
then solves it as a CSP using arc-consistency (AC-3)
followed by backtracking.
"""

from collections import deque

# ──────────────────────────────────────────────
# 1.  Constraint graph from notebook
# ──────────────────────────────────────────────
VARIABLES = ['Chennai', 'Tirupati', 'Nellore', 'Ongole']

DOMAINS = {v: ['red', 'green', 'blue'] for v in VARIABLES}

# Arcs (constraints): adjacent regions must differ
CONSTRAINTS = [
    ('Chennai',  'Tirupati'),
    ('Chennai',  'Nellore'),
    ('Tirupati', 'Nellore'),
    ('Nellore',  'Ongole'),
]

# Build adjacency for quick lookup
NEIGHBORS = {v: [] for v in VARIABLES}
for (a, b) in CONSTRAINTS:
    NEIGHBORS[a].append(b)
    NEIGHBORS[b].append(a)

# ──────────────────────────────────────────────
# 2.  AC-3 Arc Consistency
# ──────────────────────────────────────────────
def revise(domains, Xi, Xj):
    """Remove values from Xi's domain that have no support in Xj."""
    revised = False
    for x in domains[Xi][:]:
        # Check if there is any value y in Xj's domain that satisfies Xi≠Xj
        if not any(x != y for y in domains[Xj]):
            domains[Xi].remove(x)
            revised = True
    return revised

def ac3(domains):
    queue = deque()
    for (Xi, Xj) in CONSTRAINTS:
        queue.append((Xi, Xj))
        queue.append((Xj, Xi))

    print("\n--- AC-3 Arc Consistency ---")
    while queue:
        (Xi, Xj) = queue.popleft()
        if revise(domains, Xi, Xj):
            if not domains[Xi]:
                print(f"  ❌  Domain of {Xi} is empty! No solution.")
                return False
            print(f"  Domain of {Xi} reduced to {domains[Xi]}")
            for Xk in NEIGHBORS[Xi]:
                if Xk != Xj:
                    queue.append((Xk, Xi))

    print("  ✅  Arc consistency achieved.")
    return True

# ──────────────────────────────────────────────
# 3.  Backtracking with forward checking
# ──────────────────────────────────────────────
def is_consistent(var, value, assignment):
    for nb in NEIGHBORS[var]:
        if assignment.get(nb) == value:
            return False
    return True

def backtrack_csp(assignment, domains):
    if len(assignment) == len(VARIABLES):
        return assignment

    # MRV (Minimum Remaining Values) heuristic
    unassigned = [v for v in VARIABLES if v not in assignment]
    var = min(unassigned, key=lambda v: len(domains[v]))

    for value in domains[var]:
        if is_consistent(var, value, assignment):
            assignment[var] = value
            print(f"  Assign {var} = {value}")

            result = backtrack_csp(assignment, domains)
            if result is not None:
                return result

            print(f"  Backtrack from {var} = {value}")
            del assignment[var]

    return None

# ──────────────────────────────────────────────
# 4.  Display constraint graph
# ──────────────────────────────────────────────
def print_constraint_graph():
    print("Constraint Graph (adjacency):")
    for v in VARIABLES:
        print(f"  {v:<12} — {NEIGHBORS[v]}")

# ──────────────────────────────────────────────
# 5.  Main
# ──────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print("CONSTRAINT GRAPH  –  CSP Map Coloring")
    print("=" * 55)
    print_constraint_graph()

    # Step 1: AC-3
    import copy
    domains = copy.deepcopy(DOMAINS)
    ac3(domains)
    print(f"\nDomains after AC-3: {domains}")

    # Step 2: Backtracking
    print("\n--- Backtracking Search ---")
    solution = backtrack_csp({}, domains)

    print("\n" + "=" * 55)
    if solution:
        print("✅  SOLUTION FOUND:")
        color_symbols = {'red': '🔴', 'green': '🟢', 'blue': '🔵'}
        for region, color in solution.items():
            print(f"  {region:<12} →  {color_symbols.get(color,'')} {color}")

        print("\n  Constraint check:")
        for (a, b) in CONSTRAINTS:
            ok = solution[a] != solution[b]
            print(f"    {a} ≠ {b}: {solution[a]} ≠ {solution[b]}  {'✅' if ok else '❌'}")
    else:
        print("❌  No solution found.")
    print("=" * 55)
