import marimo

__generated_with = "0.23.3"
app = marimo.App(width="medium")

with app.setup:
    import collections

    import seaborn as sns


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # TDMA Slot Coloring

    **Time Division Multiple Access (TDMA)** divides time into repeating frames of fixed-length slots.
    Each node is assigned one slot per frame during which it may transmit. Nodes that share or overhear
    each other's transmissions must be assigned *different* slots to avoid collisions.

    This notebook models the problem as a **graph coloring** problem:
    1. Build the network graph from edges.
    2. Determine which node pairs *conflict* (are within 2 hops of each other).
    3. Use backtracking to enumerate all valid 5-slot colorings (schedules).
    4. Among those, find the schedule(s) that minimize end-to-end delay on a specific route.

    Let's start by defining the network edges, as in the assignment.
    """)
    return


@app.cell
def _():
    edges = [
        (1,2), (1,3), (2,3), (3,4), (4,5), (5,6),
        (6,7), (6,8), (6,9), (9,10)
    ]
    return (edges,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Build Adjacency (Neighbor) Dictionary

    We convert the edge list into an adjacency dictionary so we can quickly look up the direct
    neighbors (1-hop) of any node. Each entry maps a node to the set of nodes it is directly
    connected to.
    """)
    return


@app.cell
def _(edges):
    adj = collections.defaultdict(set)
    for _u, _v in edges:
        adj[_u].add(_v)
        adj[_v].add(_u)

    adj
    return (adj,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Build 2-Hop Conflict Graph

    In TDMA, a node's transmission is heard not only by its direct neighbors (1 hop away) but also
    potentially causes interference for nodes 2 hops away. Therefore, two nodes must use *different*
    time slots if they are within **2 hops** of each other.

    We build a `conflict` dictionary that maps every node to the full set of nodes it conflicts with
    (its 1-hop *and* 2-hop neighbors). This is the constraint graph used by the solver below.
    """)
    return


@app.cell
def _(adj):
    conflict = collections.defaultdict(set)
    for u in range(1, 11):
        for v in adj[u]:
            conflict[u].add(v) # 1 hop neighbor
            for w in adj[v]:
                if w != u:
                    conflict[u].add(w) # 2 hop neighbor

    conflict
    return (conflict,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Find All Valid Slot Assignments (Backtracking)

    We use **recursive backtracking** to enumerate every valid 5-slot TDMA schedule.
    The algorithm assigns slots to nodes one at a time (node 1 through 10). At each step it
    tries slots 1–5; a slot is *valid* if no conflicting node (within 2 hops) has already been
    assigned that same slot. When a dead end is reached the algorithm backtracks and tries the
    next slot, guaranteeing all solutions are found.
    """)
    return


@app.cell
def _(conflict):
    def solve(node, current_assignment):
        # Base case: all nodes 1-10 have been assigned a slot, so this is a complete valid schedule.
        if node > 10:
            solutions.append(current_assignment.copy())
            return

        # Try each of the 5 available time slots for the current node.
        for slot in range(1, 6):
            valid = True
            # Check that no conflicting neighbor (within 2 hops) is already using this slot.
            for neighbor in conflict[node]:
                if neighbor in current_assignment and current_assignment[neighbor] == slot:
                    valid = False
                    break

            # This slot is valid: assign it to the node and recurse to assign the next node.
            if valid:
                current_assignment[node] = slot
                solve(node + 1, current_assignment)
                # Backtrack: remove the assignment so we can try the next slot for this node.
                del current_assignment[node]

    solutions = []
    solve(1, {})
    return (solutions,)


@app.cell
def _(solutions):
    print(f"Found {len(solutions)} different acceptable 5 slot colorings.")

    # Print on of the solutions
    if solutions:
        print("Example solution", solutions[0])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Find optimal solution

    We will loop over all the 19k solutions and find the one(s) with the least timing using brute force.
    """)
    return


@app.cell
def _(solutions):
    def calculate_tdma_delay(s_u, s_v, L=5):
        """Compute the one-hop TDMA delay from node u (slot s_u) to node v (slot s_v).

        In a TDMA frame of length L, node v can only receive after it wakes up in its own slot.
        The delay is how many slots node u must wait until node v's slot comes around, wrapping
        modulo L so the frame is treated as circular.
        """
        diff = s_v - s_u
        return diff if diff > 0 else diff + L

    def get_path_delay(schedule, path, L=5):
        """Compute the total end-to-end TDMA delay along a multi-hop path.

        Sums the one-hop delays for every consecutive pair of nodes on the path.
        """
        total_delay = 0
        for i in range(len(path) - 1):
            u = path[i]
            v = path[i+1]
            total_delay += calculate_tdma_delay(schedule[u], schedule[v], L)
        return total_delay

    # The route we want to optimize: N1 -> N10 via the shortest path in the graph.
    route = [1, 3, 4, 5, 6, 9, 10]

    # Brute-force search over all valid schedules to find the minimum end-to-end delay.
    min_delay = float('inf')
    best_schedules = []

    for schedule in solutions:
        current_delay = get_path_delay(schedule, route)

        # New best found: reset the list and record this schedule.
        if current_delay < min_delay:
            min_delay = current_delay
            best_schedules = [schedule]
        # Tied with the current best: add this schedule to the list.
        elif current_delay == min_delay:
            best_schedules.append(schedule)

    print(f"Minimum possible delay for route N1 -> N10: {min_delay} time slots.")
    print(f"This optimal delay is achieved by {len(best_schedules)} different schedules.")
    print("Example optimal schedule:", best_schedules[0])
    return (get_path_delay,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Test my own solution

    During the assignment, I first solved this manually using a fairly random process. In my own calculations, I ended up in the idea that I will need 18 time slots for this. Let's verify this using code.
    """)
    return


@app.cell
def _(get_path_delay):
    # This is my own solution
    my_schedule = {
        1: 4,
        2: 2,
        3: 1,
        4: 3,
        5: 2,
        6: 1,
        7: 3,
        8: 4,
        9: 5,
        10: 2
    }

    # The shortest route
    my_route = [1, 3, 4, 5, 6, 9, 10]

    # Test this
    delay = get_path_delay(my_schedule, my_route)
    print(f"Total delay is: {delay} time slots.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Plot the distribution

    Let's use seaborn to plot the distribution (histogram) of all solutions and their delays.
    """)
    return


@app.cell
def _():
    # TODO
    return


if __name__ == "__main__":
    app.run()
