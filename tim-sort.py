import time
import random
import timeit

import pandas as pd
from matplotlib import pyplot as plt


def timSort(arr, left, right, k):
    if right - left + 1 <= k:
        insertionSortRange(arr, left, right)
    else:
        if left < right:
            mid = (left + right) // 2
            timSort(arr, left, mid, k)
            timSort(arr, mid + 1, right, k)
            merge(arr, left, mid, right)


# Implementation used from: https://www.geeksforgeeks.org/python-program-for-merge-sort/
def merge(arr, l, m, r):
    n1 = m - l + 1
    n2 = r - m

    # create temp arrays
    L = [0] * (n1)
    R = [0] * (n2)

    # Copy data to temp arrays L[] and R[]
    for i in range(0, n1):
        L[i] = arr[l + i]

    for j in range(0, n2):
        R[j] = arr[m + 1 + j]

    # Merge the temp arrays back into arr[l..r]
    i = 0  # Initial index of first subarray
    j = 0  # Initial index of second subarray
    k = l  # Initial index of merged subarray

    while i < n1 and j < n2:
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1

    # Copy the remaining elements of L[], if there
    # are any
    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1

    # Copy the remaining elements of R[], if there
    # are any
    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1

# l is for left index and r is right index of the
# sub-array of arr to be sorted
def mergeSort(arr, l, r):
    if l < r:
        # Same as (l+r)//2, but avoids overflow for
        # large l and h
        m = l + (r - l) // 2

        # Sort first and second halves
        mergeSort(arr, l, m)
        mergeSort(arr, m + 1, r)
        merge(arr, l, m, r)


# Implementation used from: https://www.geeksforgeeks.org/python-program-for-insertion-sort/
def insertionSort(arr):
    n = len(arr)  # Get the length of the array

    if n <= 1:
        return  # If the array has 0 or 1 element, it is already sorted, so return

    for i in range(1, n):  # Iterate over the array starting from the second element
        key = arr[i]  # Store the current element as the key to be inserted in the right position
        j = i - 1
        while j >= 0 and key < arr[j]:  # Move elements greater than key one position ahead
            arr[j + 1] = arr[j]  # Shift elements to the right
            j -= 1
        arr[j + 1] = key  # Insert the key in the correct position

def insertionSortRange(arr, left, right):
    for i in range(left + 1, right + 1):
        key = arr[i]
        j = i - 1
        while j >= left and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

# Wrapper functions to measure time
def tim_sort_wrapper(arr, k=32):
    timSort(arr, 0, len(arr) - 1, k)

def merge_sort_wrapper(arr):
    mergeSort(arr, 0, len(arr) - 1)

def measure_time(sort_function, arr):
    total_time = 0
    for _ in range(100):
        arr_copy = arr.copy()
        start_time = timeit.default_timer()
        sort_function(arr_copy)
        total_time += timeit.default_timer() - start_time
    return total_time / 100

def main():
    results = []
    input_sizes = list(range(1, 351, 5))  # Generates sizes from 1 to 350 with step of 5

    sorting_algorithms = {
        'Insertion Sort': insertionSort,
        'Merge Sort': merge_sort_wrapper,
        'Tim Sort': tim_sort_wrapper
    }

    for size in input_sizes:
        arr = [random.randint(0, 100000) for _ in range(size)]
        times = {}
        for name, sort_func in sorting_algorithms.items():
            if name == 'Tim Sort':
                sort_func_with_k = lambda arr: tim_sort_wrapper(arr, k=85)
                avg_time = measure_time(sort_func_with_k, arr)
            else:
                avg_time = measure_time(sort_func, arr)
            times[name] = round(avg_time, 10)
        result = {'Input Size': size}
        result.update({f"{name} Time": times[name] for name in times})
        results.append(result)

    df = pd.DataFrame(results)
    df.to_csv("tim_sort_times_k_85.csv", index=False)

    plt.figure(figsize=(10, 6))
    for name in sorting_algorithms.keys():
        plt.plot(df["Input Size"], df[f"{name} Time"], label=f"{name}", marker="o")
    plt.xlabel("Input Size (n)")
    plt.ylabel("Time (seconds)")
    plt.title("Comparison of Sorting Algorithms")
    plt.legend()
    plt.grid(True)
    plt.savefig("tim_sort_comparison_plot_k_85.png")
    plt.show()

if __name__ == '__main__':
    main()