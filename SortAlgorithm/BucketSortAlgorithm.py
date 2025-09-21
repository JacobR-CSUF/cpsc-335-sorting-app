import time
from typing import List

def bucket_sort(arr: List[float]) -> List[float]:

    n = len(arr)
    if n == 0:
        return arr
    start = time.perf_counter()

    buckets = [[] for _ in range(n)]

    for x in arr:
        idx = int(n * x)
        buckets[idx].append(x)

    for i in range(n):
        buckets[i].sort()

    result = []
    for b in buckets:
        result.extend(b)

    end = time.perf_counter()
    print(f"[Bucket] sort of {n} elements in {end-start:.6f} sec")

    return result
gpas = [0.78, 0.17, 0.26, 0.81, 0.92, 0.99, 0.68, 0.39]
print("Unsorted GPAs:", gpas)
print("sorted GPAs:", bucket_sort(gpas))