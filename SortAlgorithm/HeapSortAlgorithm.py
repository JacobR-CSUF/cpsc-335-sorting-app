def heap_sort(arr):
    def sift_down(a, start, end):
        root = start
        while (left :=2 * root +1) <= end:
            right = left +1
            largest = root
            if a[left] > a[largest]:
                largest = left

            if right <= end and a[right] > a[largest]:
                largest = right
            if largest == root:
                break
            a[root], a[largest] = a[largest], a[root]
            root = largest

    def build_max_heap(a):
        n= len(a)
        for i in range(n // 2 - 1, -1, -1):
            sift_down(a, i, n -1 )

    a = arr
    n = len(a)
    build_max_heap(a)
    for end in range(n-1, 0, -1):
        a[0], a[end] = a[end], a[0]
        sift_down(a, 0, end -1)

    return a

if __name__ == "__main__":
    data = [23, 77, 10, 12, 50, 60, 9]
    print("Unsorted Data:", data)
    sorted_data = heap_sort(data)
    print("Sorted Data:", sorted_data)
    