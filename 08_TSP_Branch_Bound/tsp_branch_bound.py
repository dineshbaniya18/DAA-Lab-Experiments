import math
import heapq


def reduce_matrix(matrix):
    n = len(matrix)
    reduction_cost = 0

    # Row reduction
    for i in range(n):
        row_min = min(
            (matrix[i][j] for j in range(n)
             if matrix[i][j] != math.inf),
            default=0
        )

        if row_min > 0:
            reduction_cost += row_min

            for j in range(n):
                if matrix[i][j] != math.inf:
                    matrix[i][j] -= row_min

    # Column reduction
    for j in range(n):
        col_min = min(
            (matrix[i][j] for i in range(n)
             if matrix[i][j] != math.inf),
            default=0
        )

        if col_min > 0:
            reduction_cost += col_min

            for i in range(n):
                if matrix[i][j] != math.inf:
                    matrix[i][j] -= col_min

    return reduction_cost


def tsp_branch_and_bound(cost):
    n = len(cost)

    root_matrix = [
        [math.inf if cost[i][j] == math.inf else cost[i][j]
         for j in range(n)]
        for i in range(n)
    ]

    root_bound = reduce_matrix(root_matrix)

    # Heap entry:
    # (bound, current_cost, current_city, path, matrix)
    heap = [
        (root_bound, 0, 0, [0], root_matrix)
    ]

    best_cost = math.inf
    best_path = None

    while heap:
        bound, current_cost, current_city, path, matrix = heapq.heappop(heap)

        if bound >= best_cost:
            continue

        if len(path) == n:
            final_cost = current_cost + cost[current_city][0]

            if final_cost < best_cost:
                best_cost = final_cost
                best_path = path + [0]

            continue

        for next_city in range(n):

            if next_city in path:
                continue

            if cost[current_city][next_city] == math.inf:
                continue

            new_matrix = [
                row[:] for row in matrix
            ]

            # Block current row
            for j in range(n):
                new_matrix[current_city][j] = math.inf

            # Block next city column
            for i in range(n):
                new_matrix[i][next_city] = math.inf

            # Prevent returning to the start before all cities are visited
            new_matrix[next_city][0] = math.inf

            reduction = reduce_matrix(new_matrix)

            new_cost = (
                current_cost
                + cost[current_city][next_city]
            )

            new_bound = new_cost + reduction

            if new_bound < best_cost:
                heapq.heappush(
                    heap,
                    (
                        new_bound,
                        new_cost,
                        next_city,
                        path + [next_city],
                        new_matrix
                    )
                )

    return best_path, best_cost


def brute_force_tsp(cost):
    """Verification using brute force."""
    from itertools import permutations

    n = len(cost)
    best_cost = math.inf
    best_path = None

    for perm in permutations(range(1, n)):
        path = [0] + list(perm) + [0]

        total = 0
        valid = True

        for i in range(len(path) - 1):
            edge = cost[path[i]][path[i + 1]]

            if edge == math.inf:
                valid = False
                break

            total += edge

        if valid and total < best_cost:
            best_cost = total
            best_path = path

    return best_path, best_cost


# ---------------------------------------------------------
# Experiment 8: Travelling Salesman Problem
# ---------------------------------------------------------

INF = math.inf

cost_matrix = [
    [INF, 10, 15, 20, 8],
    [10, INF, 9, 12, 6],
    [15, 9, INF, 7, 11],
    [20, 12, 7, INF, 8],
    [8, 6, 11, 8, INF]
]

cities = ['A', 'B', 'C', 'D', 'E']

print("Travelling Salesman Problem")
print("----------------------------------------")

path, cost = tsp_branch_and_bound(cost_matrix)

print("Optimal Tour:", " -> ".join(cities[i] for i in path))
print("Minimum Cost:", cost)

print("\nBrute Force Verification")
print("----------------------------------------")

verify_path, verify_cost = brute_force_tsp(cost_matrix)

print(
    "Verified Tour:",
    " -> ".join(cities[i] for i in verify_path)
)
print("Verified Cost:", verify_cost)