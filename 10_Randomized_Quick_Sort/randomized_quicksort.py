import random
import sys
sys.setrecursionlimit(20000)
import time


class ComparisonCounter:
    def __init__(self):
        self.count = 0


def partition(arr, low, high, counter):
    pivot = arr[high]

    i = low - 1

    for j in range(low, high):
        counter.count += 1

        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]

    return i + 1


def deterministic_quick_sort(arr, low, high, counter):
    if low < high:
        pivot_index = partition(arr, low, high, counter)

        deterministic_quick_sort(arr, low, pivot_index - 1, counter)
        deterministic_quick_sort(arr, pivot_index + 1, high, counter)


def randomized_partition(arr, low, high, counter):
    random_index = random.randint(low, high)

    arr[random_index], arr[high] = arr[high], arr[random_index]

    return partition(arr, low, high, counter)


def randomized_quick_sort(arr, low, high, counter):
    if low < high:
        pivot_index = randomized_partition(arr, low, high, counter)

        randomized_quick_sort(arr, low, pivot_index - 1, counter)
        randomized_quick_sort(arr, pivot_index + 1, high, counter)


def generate_test_cases(n):
    random_case = list(range(n))
    random.shuffle(random_case)

    sorted_case = list(range(n))

    reverse_case = list(range(n - 1, -1, -1))

    nearly_sorted_case = list(range(n))

    for _ in range(n // 100):
        i = random.randint(0, n - 1)
        j = random.randint(0, n - 1)
        nearly_sorted_case[i], nearly_sorted_case[j] = (
            nearly_sorted_case[j],
            nearly_sorted_case[i]
        )

    return {
        "Random": random_case,
        "Sorted": sorted_case,
        "Reverse-Sorted": reverse_case,
        "Nearly-Sorted": nearly_sorted_case
    }


def measure_algorithm(sort_function, data):
    arr = data.copy()
    counter = ComparisonCounter()

    start = time.perf_counter()

    sort_function(arr, 0, len(arr) - 1, counter)

    end = time.perf_counter()

    return counter.count, end - start


N = 10000

print("=" * 70)
print("EXPERIMENT 10: RANDOMIZED QUICK SORT")
print("=" * 70)
print(f"Array size: {N}")

test_cases = generate_test_cases(N)

for name, data in test_cases.items():
    print("\n" + "-" * 70)
    print(f"Input Type: {name}")
    print("-" * 70)

    deterministic_comparisons, deterministic_time = measure_algorithm(
        deterministic_quick_sort, data
    )

    randomized_comparisons, randomized_time = measure_algorithm(
        randomized_quick_sort, data
    )

    print(
        f"Deterministic Quick Sort : "
        f"Comparisons = {deterministic_comparisons}, "
        f"Time = {deterministic_time:.6f} seconds"
    )

    print(
        f"Randomized Quick Sort    : "
        f"Comparisons = {randomized_comparisons}, "
        f"Time = {randomized_time:.6f} seconds"
    )

print("\n" + "=" * 70)
print("Experiment completed successfully.")
print("=" * 70)
