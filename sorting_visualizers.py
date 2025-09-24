"""
Sorting algorithm visualization generators
"""

class SortingVisualizers:
    @staticmethod
    def bubble_sort_visual(sorting_array, app_instance):
        """Generator for bubble sort visualization"""
        n = len(sorting_array)

        for i in range(n):
            swapped = False

            for j in range(0, n-i-1):
                if not app_instance.sorting:
                    yield False

                while app_instance.paused:
                    yield True

                app_instance.current_indices = [j, j+1]

                if sorting_array[j] > sorting_array[j+1]:
                    sorting_array[j], sorting_array[j+1] = sorting_array[j+1], sorting_array[j]
                    swapped = True

                yield True

            if not swapped:
                break

        app_instance.complete_sorting()
        app_instance.sorted = True
        app_instance.sorting = False
        app_instance.current_indices = []
        yield False

    @staticmethod
    def bucket_sort_visual(sorting_array, app_instance):
        """Generator for bucket sort visualization (adapted for integers)"""
        n = len(sorting_array)
        if n == 0:
            yield False
            return

        # Find range for normalization
        min_val = min(sorting_array)
        max_val = max(sorting_array)
        range_val = max_val - min_val + 1

        # Create buckets
        bucket_count = min(n, 10)  # Use 10 buckets or less
        buckets = [[] for _ in range(bucket_count)]

        # Distribute elements into buckets
        for i, x in enumerate(sorting_array):
            if not app_instance.sorting:
                yield False
                return
            while app_instance.paused:
                yield True

            # Normalize to bucket index
            normalized = (x - min_val) / range_val
            idx = min(int(bucket_count * normalized), bucket_count - 1)
            buckets[idx].append(x)
            app_instance.current_indices = [i]
            yield True

        # Sort each bucket and reconstruct array
        result_idx = 0
        for bucket in buckets:
            if bucket:
                bucket.sort()
                for value in bucket:
                    if not app_instance.sorting:
                        yield False
                        return
                    while app_instance.paused:
                        yield True

                    sorting_array[result_idx] = value
                    app_instance.current_indices = [result_idx]
                    result_idx += 1
                    yield True

        app_instance.complete_sorting()
        app_instance.sorted = True
        app_instance.sorting = False
        app_instance.current_indices = []
        yield False

    @staticmethod
    def counting_sort_visual(sorting_array, app_instance):
        """Generator for counting sort visualization"""
        if not sorting_array:
            yield False
            return

        max_val = max(sorting_array)
        min_val = min(sorting_array)
        k = max_val - min_val + 1

        # Counting phase
        count = [0] * k
        for i, num in enumerate(sorting_array):
            if not app_instance.sorting:
                yield False
                return
            while app_instance.paused:
                yield True

            count[num - min_val] += 1
            app_instance.current_indices = [i]
            yield True

        # Reconstruction phase
        output_idx = 0
        for i, freq in enumerate(count):
            value = i + min_val
            for _ in range(freq):
                if not app_instance.sorting:
                    yield False
                    return
                while app_instance.paused:
                    yield True

                sorting_array[output_idx] = value
                app_instance.current_indices = [output_idx]
                output_idx += 1
                yield True

        app_instance.complete_sorting()
        app_instance.sorted = True
        app_instance.sorting = False
        app_instance.current_indices = []
        yield False

    @staticmethod
    def quick_select_visual(sorting_array, app_instance):
        """Generator for quick select visualization (optimized implementation)"""
        n = len(sorting_array)
        yield from SortingVisualizers._quick_select_sort_visual(
            sorting_array, 0, n - 1, app_instance
        )

        app_instance.complete_sorting()
        app_instance.sorted = True
        app_instance.sorting = False
        app_instance.current_indices = []
        yield False

    @staticmethod
    def _quick_select_sort_visual(arr, low, high, app_instance):
        """Optimized quick select based sorting with proper time complexity"""
        if low < high:
            # Use the same partitioning as your reference implementation
            pivot_idx = yield from SortingVisualizers._partition_visual(arr, low, high, app_instance)

            if not app_instance.sorting:
                yield False
                return

            # Recursively sort both partitions (similar to quicksort but with quickselect partitioning)
            yield from SortingVisualizers._quick_select_sort_visual(arr, low, pivot_idx - 1, app_instance)
            yield from SortingVisualizers._quick_select_sort_visual(arr, pivot_idx + 1, high, app_instance)

    @staticmethod
    def _partition_visual(arr, low, high, app_instance):
        """Partition function matching your reference implementation with visualization"""
        pivot = arr[high]  # Choose last element as pivot (matches your reference)
        i = low

        for j in range(low, high):
            if not app_instance.sorting:
                yield False
                return i
            while app_instance.paused:
                yield True

            app_instance.current_indices = [j, high, i]  # Highlight current element, pivot, and partition index

            if arr[j] <= pivot:
                if i != j:  # Only swap if different indices
                    arr[i], arr[j] = arr[j], arr[i]
                    app_instance.current_indices = [i, j]
                    yield True
                i += 1

            yield True

        # Place pivot in correct position (matches your reference)
        if i != high:
            arr[i], arr[high] = arr[high], arr[i]
            app_instance.current_indices = [i, high]
            yield True

        return i

    @staticmethod
    def _quick_select_helper_visual(arr, low, high, k, app_instance):
        """Updated helper that matches your reference implementation exactly"""
        if low <= high:
            # Use the same partition function as the main implementation
            pi = yield from SortingVisualizers._partition_visual(arr, low, high, app_instance)

            if not app_instance.sorting:
                yield False
                return

            if pi == k:
                # Found k-th element - highlight it
                app_instance.current_indices = [pi]
                yield True
                return
            elif pi > k:
                # k-th element is in left partition
                yield from SortingVisualizers._quick_select_helper_visual(
                    arr, low, pi - 1, k, app_instance
                )
            else:
                # k-th element is in right partition
                yield from SortingVisualizers._quick_select_helper_visual(
                    arr, pi + 1, high, k, app_instance
                )

    @staticmethod
    def heap_sort_visual(sorting_array, app_instance):
        """Generator for heap sort visualization"""
        n = len(sorting_array)

        # Build max heap
        for i in range(n // 2 - 1, -1, -1):
            yield from SortingVisualizers._sift_down_visual(sorting_array, i, n - 1, app_instance)

        # Extract elements from heap
        for end in range(n - 1, 0, -1):
            if not app_instance.sorting:
                yield False
                return
            while app_instance.paused:
                yield True

            # Swap root with end
            sorting_array[0], sorting_array[end] = sorting_array[end], sorting_array[0]
            app_instance.current_indices = [0, end]
            yield True

            # Sift down the new root
            yield from SortingVisualizers._sift_down_visual(sorting_array, 0, end - 1, app_instance)

        app_instance.complete_sorting()
        app_instance.sorted = True
        app_instance.sorting = False
        app_instance.current_indices = []
        yield False

    @staticmethod
    def _sift_down_visual(a, start, end, app_instance):
        """Helper for heap sort sift down with visualization"""
        root = start
        while (left := 2 * root + 1) <= end:
            if not app_instance.sorting:
                yield False
                return
            while app_instance.paused:
                yield True

            right = left + 1
            largest = root

            if a[left] > a[largest]:
                largest = left
            if right <= end and a[right] > a[largest]:
                largest = right

            if largest == root:
                break

            a[root], a[largest] = a[largest], a[root]
            app_instance.current_indices = [root, largest]
            yield True

            root = largest

    @staticmethod
    def insertion_sort_visual(sorting_array, app_instance):
        """Generator for insertion sort visualization"""
        n = len(sorting_array)

        for i in range(1, n):
            key = sorting_array[i]
            j = i - 1

            while j >= 0 and sorting_array[j] > key:
                if not app_instance.sorting:
                    yield False
                    return
                while app_instance.paused:
                    yield True

                sorting_array[j + 1] = sorting_array[j]
                app_instance.current_indices = [j, j + 1]
                j -= 1
                yield True

            sorting_array[j + 1] = key
            app_instance.current_indices = [j + 1]
            yield True

        app_instance.complete_sorting()
        app_instance.sorted = True
        app_instance.sorting = False
        app_instance.current_indices = []
        yield False

    @staticmethod
    def merge_sort_visual(sorting_array, app_instance):
        """Generator for merge sort visualization"""
        yield from SortingVisualizers._merge_sort_helper(sorting_array, 0, len(sorting_array) - 1, app_instance)

        app_instance.complete_sorting()
        app_instance.sorted = True
        app_instance.sorting = False
        app_instance.current_indices = []
        yield False

    @staticmethod
    def _merge_sort_helper(arr, left, right, app_instance):
        """Recursive helper for merge sort with visualization"""
        if left >= right:
            return

        mid = (left + right) // 2

        # Sort left half
        yield from SortingVisualizers._merge_sort_helper(arr, left, mid, app_instance)

        # Sort right half
        yield from SortingVisualizers._merge_sort_helper(arr, mid + 1, right, app_instance)

        # Merge the sorted halves
        yield from SortingVisualizers._merge_visual(arr, left, mid, right, app_instance)

    @staticmethod
    def _merge_visual(arr, left, mid, right, app_instance):
        """Merge with visualization"""
        left_arr = arr[left:mid + 1]
        right_arr = arr[mid + 1:right + 1]

        i = j = 0
        k = left

        while i < len(left_arr) and j < len(right_arr):
            if not app_instance.sorting:
                yield False
                return
            while app_instance.paused:
                yield True

            if left_arr[i] <= right_arr[j]:
                arr[k] = left_arr[i]
                i += 1
            else:
                arr[k] = right_arr[j]
                j += 1

            app_instance.current_indices = [k]
            k += 1
            yield True

        while i < len(left_arr):
            if not app_instance.sorting:
                yield False
                return
            while app_instance.paused:
                yield True

            arr[k] = left_arr[i]
            app_instance.current_indices = [k]
            i += 1
            k += 1
            yield True

        while j < len(right_arr):
            if not app_instance.sorting:
                yield False
                return
            while app_instance.paused:
                yield True

            arr[k] = right_arr[j]
            app_instance.current_indices = [k]
            j += 1
            k += 1
            yield True

    @staticmethod
    def quick_sort_visual(sorting_array, app_instance):
        """Generator for quick sort visualization"""
        yield from SortingVisualizers._quick_sort_helper(sorting_array, 0, len(sorting_array) - 1, app_instance)

        app_instance.complete_sorting()
        app_instance.sorted = True
        app_instance.sorting = False
        app_instance.current_indices = []
        yield False

    @staticmethod
    def _quick_sort_helper(arr, low, high, app_instance):
        """Recursive helper for quick sort with visualization"""
        if low < high:
            # Partition
            pivot = arr[(low + high) // 2]
            i = low
            j = high

            while i <= j:
                if not app_instance.sorting:
                    yield False
                    return
                while app_instance.paused:
                    yield True

                while arr[i] < pivot:
                    i += 1
                while arr[j] > pivot:
                    j -= 1

                if i <= j:
                    arr[i], arr[j] = arr[j], arr[i]
                    app_instance.current_indices = [i, j]
                    yield True
                    i += 1
                    j -= 1

            # Recursively sort partitions
            yield from SortingVisualizers._quick_sort_helper(arr, low, j, app_instance)
            yield from SortingVisualizers._quick_sort_helper(arr, i, high, app_instance)

    @staticmethod
    def radix_sort_visual(sorting_array, app_instance):
        """Generator for radix sort visualization"""
        if not sorting_array:
            yield False
            return

        # Handle negative numbers separately
        neg = []
        pos = []
        for i, x in enumerate(sorting_array):
            if x < 0:
                neg.append(-x)
            else:
                pos.append(x)

        # Sort positive numbers
        if pos:
            max_val = max(pos)
            exp = 1
            base = 10

            while max_val // exp > 0:
                yield from SortingVisualizers._counting_sort_by_digit_visual(
                    pos, exp, base, sorting_array, False, app_instance
                )
                exp *= base

        # Sort negative numbers
        if neg:
            max_val = max(neg)
            exp = 1
            base = 10

            while max_val // exp > 0:
                yield from SortingVisualizers._counting_sort_by_digit_visual(
                    neg, exp, base, sorting_array, True, app_instance
                )
                exp *= base
            neg.reverse()

        # Reconstruct the array
        result = [-x for x in neg] + pos
        for i, val in enumerate(result):
            if not app_instance.sorting:
                yield False
                return
            while app_instance.paused:
                yield True

            sorting_array[i] = val
            app_instance.current_indices = [i]
            yield True

        app_instance.complete_sorting()
        app_instance.sorted = True
        app_instance.sorting = False
        app_instance.current_indices = []
        yield False

    @staticmethod
    def _counting_sort_by_digit_visual(a, exp, base, original_array, is_negative, app_instance):
        """Helper for radix sort digit sorting with visualization"""
        n = len(a)
        output = [0] * n
        count = [0] * base

        # Count occurrences
        for i in range(n):
            if not app_instance.sorting:
                yield False
                return
            while app_instance.paused:
                yield True

            digit = (a[i] // exp) % base
            count[digit] += 1
            yield True

        # Calculate positions
        for d in range(1, base):
            count[d] += count[d - 1]

        # Build output array
        for i in range(n - 1, -1, -1):
            if not app_instance.sorting:
                yield False
                return
            while app_instance.paused:
                yield True

            digit = (a[i] // exp) % base
            pos = count[digit] - 1
            output[pos] = a[i]
            count[digit] -= 1
            yield True

        # Copy back
        for i in range(n):
            a[i] = output[i]
