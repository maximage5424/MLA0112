"""
Hill Climbing - Blocks World Problem
-------------------------------------
Start: [A, B, C, D] stacked (A on top, D at bottom)
Goal:  [D, C, B, A] stacked (D on top, A at bottom)

Heuristic scoring:
  - Each block in WRONG order  => -1 (negative)
  - Each block in CORRECT order => +1 (positive)
"""

# ──────────────────────────────────────────────
# 1.  Heuristic
# ──────────────────────────────────────────────
def heuristic(state, goal):
    """
    Compare state stack with goal stack from bottom to top.
    +1  for every position that matches the goal
    -1  for every position that does NOT match
    """
    score = 0
    for i in range(len(goal)):
        if i < len(state) and state[i] == goal[i]:
            score += 1   # correct order  → +ve
        else:
            score -= 1   # wrong order    → -ve
    return score


# ──────────────────────────────────────────────
# 2.  Generate neighbours
#     Allowed move: pick the TOP block of any
#     stack and place it on top of another stack
#     or on the table as a new single-block stack.
# ──────────────────────────────────────────────
def get_neighbors(stacks):
    neighbors = []
    for i, stack in enumerate(stacks):
        if not stack:
            continue
        # pick top block from stack i
        block = stack[-1]
        new_stacks_base = [s[:] for s in stacks]
        new_stacks_base[i].pop()

        # place it on every other stack
        for j in range(len(stacks)):
            if i == j:
                continue
            new_stacks = [s[:] for s in new_stacks_base]
            new_stacks[j].append(block)
            neighbors.append(new_stacks)

        # place it as a brand-new stack on the table
        new_stacks = [s[:] for s in new_stacks_base]
        new_stacks.append([block])
        neighbors.append(new_stacks)

    # remove empty stacks
    neighbors = [[s for s in n if s] for n in neighbors]
    return neighbors


# ──────────────────────────────────────────────
# 3.  Hill Climbing
# ──────────────────────────────────────────────
def hill_climbing(start_stacks, goal_stack, max_iterations=100):
    """
    start_stacks : list of lists  e.g. [['D','C','B','A']]
                   index 0 = bottom, last index = top
    goal_stack   : single list    e.g. ['A','B','C','D']
                   index 0 = bottom, last index = top
    """
    current = [s[:] for s in start_stacks]
    current_score = heuristic(current[0] if len(current) == 1 else [], goal_stack)

    print("=" * 55)
    print("HILL CLIMBING  –  Blocks World")
    print("=" * 55)
    print(f"Start  : {current}   score={heuristic(current[0], goal_stack)}")
    print(f"Goal   : {[goal_stack]}")
    print("-" * 55)

    for iteration in range(1, max_iterations + 1):
        neighbors = get_neighbors(current)
        if not neighbors:
            print("No neighbours found. Stopping.")
            break

        # score each neighbour (use the tallest / only stack for heuristic)
        best_neighbor = None
        best_score = current_score

        for nb in neighbors:
            # find the stack that matches goal length for scoring
            main_stack = max(nb, key=len) if nb else []
            score = heuristic(main_stack, goal_stack)
            if score > best_score:
                best_score = score
                best_neighbor = nb

        if best_neighbor is None:
            print(f"Step {iteration}: Local maximum reached. Score = {current_score}")
            break

        current = best_neighbor
        current_score = best_score
        main = max(current, key=len)

        print(f"Step {iteration}: stacks={current}   score={current_score}")

        # goal check
        if len(current) == 1 and current[0] == goal_stack:
            print("-" * 55)
            print(f"✅  GOAL REACHED in {iteration} step(s)!")
            break
    else:
        print("Max iterations reached without finding goal.")

    print("=" * 55)
    return current


# ──────────────────────────────────────────────
# 4.  Main
# ──────────────────────────────────────────────
if __name__ == "__main__":
    # Stack representation: index 0 = bottom, last = top
    # Start: D(bottom) → C → B → A(top)
    start = [['D', 'C', 'B', 'A']]

    # Goal:  A(bottom) → B → C → D(top)
    goal  =  ['A', 'B', 'C', 'D']

    print("\nBlocks World scoring legend:")
    print("  Wrong order  → -1 per block")
    print("  Correct order → +1 per block\n")

    result = hill_climbing(start, goal)
    print(f"\nFinal state : {result}")
