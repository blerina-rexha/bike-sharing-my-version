
import timeit
from collections.abc import Callable
from typing import Any


# ---------------------------------------------------------------------------
# Sorting — Merge Sort
# ---------------------------------------------------------------------------

def merge_sort(data: list[Any], key: Callable = lambda x: x) -> list[Any]:
  
    if len(data) <= 1:
        return list(data)

    mid = len(data) // 2
    left = merge_sort(data[:mid], key=key)
    right = merge_sort(data[mid:], key=key)

    return _merge(left, right, key=key)


def _merge(
    left: list[Any], right: list[Any], key: Callable
) -> list[Any]:
    """Merge two sorted lists into one sorted list."""
    result: list[Any] = []
    i = j = 0

    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


# ---------------------------------------------------------------------------
# Sorting — Insertion Sort 
# ---------------------------------------------------------------------------

def insertion_sort(data: list[Any], key: Callable = lambda x: x) -> list[Any]:
    #Sort *data* using the insertion-sort algorithm.

    a=data.copy()
    for i in range(1,len(a)):
        current=a[i]
        j=i-1
        while j>=0 and key(a[j])>key(current):
            a[j+1]=a[j]
            j-=1
        a[j+1]=current
    return a

# ---------------------------------------------------------------------------
# Searching — Binary Search 
# ---------------------------------------------------------------------------

def binary_search(
    sorted_data: list[Any],
    target: Any,
    key: Callable = lambda x: x,
) -> int | None:
    #Search for *target* in *sorted_data* using binary search.
    low, high = 0, len(sorted_data) - 1

    while low <= high:
        mid = (low + high) // 2
        mid_val = key(sorted_data[mid])

        if mid_val == target:
            return mid
        elif mid_val < target:
            low = mid + 1
        else:
            high = mid - 1
    return None

# ---------------------------------------------------------------------------
# Searching — Linear Search
# ---------------------------------------------------------------------------

def linear_search(
    data: list[Any],
    target: Any,
    key: Callable = lambda x: x,
) -> int | None:
    #Search for *target* in *data* using linear search.
    low, high = 0, len(data) - 1
    while low <= high:
        mid = (low + high) // 2
        mid_val = key(sorted_data[mid])

        if mid_val == target:
            return mid
        elif mid_val < target:
            low = mid + 1
        else:
            high = mid - 1
    return None
# ---------------------------------------------------------------------------
# Benchmarking helper
# ---------------------------------------------------------------------------

def benchmark_sort(data: list, key: Callable = lambda x: x, repeats: int = 5) -> dict:
    #Compare custom merge_sort vs. built-in sorted.
    custom_time = timeit.timeit(
        lambda: merge_sort(data, key=key), number=repeats
    )
    builtin_time = timeit.timeit(
        lambda: sorted(data, key=key), number=repeats
    )

    return {
        "merge_sort_ms": round(custom_time / repeats * 1000, 2),
        "builtin_sorted_ms": round(builtin_time / repeats * 1000, 2),
    }


def benchmark_search(
    data: list,
    target: Any,
    key: Callable = lambda x: x,
    repeats: int = 5,
) -> dict:
    #Compare binary_search, linear_search, and built-in 'in'.
    sorted_data = sorted(data, key=key)
    binary_time = timeit.timeit(
        lambda: binary_search(sorted_data, target, key=key), number=repeats
    )

    linear_time = timeit.timeit(
        lambda: linear_search(data, target, key=key), number=repeats
    )

    builtin_time = timeit.timeit(
        lambda: target in data, number=repeats   
    )

    return {
        "binary_search_ms": round(binary_time / repeats * 1000, 2), 
        "linear_search_ms": round(linear_time / repeats * 1000, 2),
        "builtin_in_ms": round(builtin_time / repeats * 1000, 2),
    }
