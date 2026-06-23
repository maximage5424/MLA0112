"""
Map Coloring  –  CSP  (Image 3)
=================================
Problem: Nearby states/regions cannot have the same colour.

Regions from notebook:
  Chennai, Tirupathi (Tirupati), Nellore, Hyderabad, Ongole (Arm)

Constraints (edges – shared borders):
  Chennai    – Tirupati
  Chennai    – Nellore
  Tirupati   – Nellore
  Tirupati   – Hyderabad
  Nellore    – Ongole
  Hyderabad  – Ongole

Available colours: red, green, blue
"""

# ──────────────────────────────────────────────
# 1.  Problem definition
# ──────────────────────────────────────────────
REGIONS = ['Chennai', 'Tirupati', 'Nellore', 'Hyderabad', 'Ongole']

NEIGHBORS = {
    'Chennai':   ['Tirupati', 'Nellore'],
    'Tirupati':  ['Chennai', 'Nellore', 'Hyderabad'],
    'Nellore':   ['Chennai', 'Tirupati', 'Ongole'],
    'Hyderabad': ['Tirupati', 'Ongole'],
    'Ongole':    ['Nellore', 'Hyderabad'],
}

COLORS = ['red', 'green', 'blue']

# ──────────────────────────────────────────────
# 2.  Constraint check
# ──────────────────────────────────────────────
def is_valid(region, color, assignment):
    """Return True if 'color' doesn't conflict with already-assigned neighbors."""
    for neighbor in NEIGHBORS[region]:
        if assignment.get(neighbor) == color:
            return False
    return True

# ──────────────────────────────────────────────
# 3.  Backtracking CSP solver
# ──────────────────────────────────────────────
def backtrack(assignment, regions):
    # Base case: all regions assigned
    if len(assignment) == len(regions):
        return assignment

    # Choose next unassigned region (in order)
    unassigned = [r for r in regions if r not in assignment]
    region = unassigned[0]

    print(f"\nAssigning color to: {region}")

    for color in COLORS:
        if is_valid(region, color, assignment):
            assignment[region] = color
            print(f"  ✅  {region} = {color}")

            result = backtrack(assignment, regions)
            if result is not None:
                return result

            # Backtrack
            print(f"  ❌  Backtrack from {region} = {color}")
            del assignment[region]

    return None   # failure

# ──────────────────────────────────────────────
# 4.  Display result
# ──────────────────────────────────────────────
def display_coloring(assignment):
    print("\n" + "=" * 45)
    print("FINAL MAP COLORING")
    print("=" * 45)
    color_symbols = {'red': '🔴', 'green': '🟢', 'blue': '🔵'}
    for region, color in assignment.items():
        print(f"  {region:<12} →  {color_symbols.get(color, '')} {color}")
    print("=" * 45)

    # Verify constraints
    print("\nConstraint verification:")
    all_ok = True
    for region, neighbors in NEIGHBORS.items():
        for nb in neighbors:
            if assignment.get(region) == assignment.get(nb):
                print(f"  ❌  CONFLICT: {region} and {nb} both = {assignment[region]}")
                all_ok = False
    if all_ok:
        print("  ✅  All constraints satisfied!")

# ──────────────────────────────────────────────
# 5.  Main
# ──────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 45)
    print("MAP COLORING  –  CSP with Backtracking")
    print(f"  Regions : {REGIONS}")
    print(f"  Colors  : {COLORS}")
    print("=" * 45)
    print("\nConstraint: Neighboring regions ≠ same color")

    solution = backtrack({}, REGIONS)

    if solution:
        display_coloring(solution)
    else:
        print("❌  No valid coloring found.")
