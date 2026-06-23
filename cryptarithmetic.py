"""
Cryptarithmetic Problem  (Images 4 & 6)
=========================================
    S E N D
  + M O R E
  ---------
  M O N E Y

Each letter = unique digit (0-9)
From notebook:  S=9, M=1, O=0  (partial assignment shown)

Constraints:
  - All letters represent different digits
  - M ≠ 0 (leading digit)
  - S ≠ 0 (leading digit)
  - SEND + MORE = MONEY
"""

from itertools import permutations

# ──────────────────────────────────────────────
# 1.  Brute-force solver
# ──────────────────────────────────────────────
def solve_cryptarithmetic():
    print("=" * 50)
    print("CRYPTARITHMETIC  –  SEND + MORE = MONEY")
    print("=" * 50)
    print("  Unique letters: S E N D M O R Y")
    print("  Constraints  : S≠0, M≠0, all digits unique")
    print("-" * 50)

    letters = ['S', 'E', 'N', 'D', 'M', 'O', 'R', 'Y']
    solutions = []

    # Try all permutations of 8 digits from 0-9
    for perm in permutations(range(10), 8):
        S, E, N, D, M, O, R, Y = perm

        # Leading digit constraints
        if S == 0 or M == 0:
            continue

        SEND  = S*1000 + E*100 + N*10 + D
        MORE  = M*1000 + O*100 + R*10 + E
        MONEY = M*10000 + O*1000 + N*100 + E*10 + Y

        if SEND + MORE == MONEY:
            solutions.append({
                'S': S, 'E': E, 'N': N, 'D': D,
                'M': M, 'O': O, 'R': R, 'Y': Y,
                'SEND': SEND, 'MORE': MORE, 'MONEY': MONEY
            })

    return solutions

# ──────────────────────────────────────────────
# 2.  Constraint propagation (manual from notebook)
# ──────────────────────────────────────────────
def solve_with_constraints():
    """
    From the notebook partial solution:
      0 = O
      1 = M
      9 = S
    Use these as fixed values and solve for rest.
    """
    print("\n--- Solving with notebook constraints (S=9, M=1, O=0) ---")
    letters = ['S', 'E', 'N', 'D', 'M', 'O', 'R', 'Y']
    fixed = {'S': 9, 'M': 1, 'O': 0}
    remaining_digits = [d for d in range(10) if d not in fixed.values()]
    free_letters = [l for l in letters if l not in fixed]

    for perm in permutations(remaining_digits, len(free_letters)):
        assign = dict(zip(free_letters, perm))
        assign.update(fixed)

        S, E, N, D = assign['S'], assign['E'], assign['N'], assign['D']
        M, O, R, Y = assign['M'], assign['O'], assign['R'], assign['Y']

        SEND  = S*1000 + E*100 + N*10 + D
        MORE  = M*1000 + O*100 + R*10 + E
        MONEY = M*10000 + O*1000 + N*100 + E*10 + Y

        if SEND + MORE == MONEY:
            print(f"\n✅  Solution found with notebook constraints!")
            return {**assign, 'SEND': SEND, 'MORE': MORE, 'MONEY': MONEY}

    return None

# ──────────────────────────────────────────────
# 3.  Display
# ──────────────────────────────────────────────
def display_solution(sol):
    print(f"\n  Letter assignments:")
    for k in ['S', 'E', 'N', 'D', 'M', 'O', 'R', 'Y']:
        print(f"    {k} = {sol[k]}")
    print(f"\n    {sol['SEND']:>6}   (SEND)")
    print(f"  + {sol['MORE']:>6}   (MORE)")
    print(f"  {'='*9}")
    print(f"  {sol['MONEY']:>7}   (MONEY)")
    print(f"\n  Verification: {sol['SEND']} + {sol['MORE']} = {sol['MONEY']}  "
          f"{'✅' if sol['SEND'] + sol['MORE'] == sol['MONEY'] else '❌'}")

# ──────────────────────────────────────────────
# 4.  Main
# ──────────────────────────────────────────────
if __name__ == "__main__":
    solutions = solve_cryptarithmetic()

    if solutions:
        print(f"\n✅  Found {len(solutions)} solution(s):\n")
        for i, sol in enumerate(solutions, 1):
            print(f"--- Solution {i} ---")
            display_solution(sol)
    else:
        print("❌  No solution found.")

    print("\n" + "=" * 50)
    # Solve with notebook's partial constraints
    constrained_sol = solve_with_constraints()
    if constrained_sol:
        display_solution(constrained_sol)
    print("=" * 50)
