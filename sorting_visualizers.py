"""
Sorting algorithm visualization generators
Uses algorithms from SortAlgorithm folder
"""

from SortAlgorithm.BubbleSortAlgorithm import bubble_sort

class SortingVisualizers:
    @staticmethod
    def bubble_sort_visual(sorting_array, app_instance):
        """
        Generator for bubble sort visualization
        No longer outputs step-by-step time messages
        """
        n = len(sorting_array)

        for i in range(n):
            swapped = False

            for j in range(0, n-i-1):
                if not app_instance.sorting:
                    yield False

                # Check if paused (but don't stop the generator)
                while app_instance.paused:
                    yield True  # Keep yielding while paused

                app_instance.current_indices = [j, j+1]

                if sorting_array[j] > sorting_array[j+1]:
                    sorting_array[j], sorting_array[j+1] = sorting_array[j+1], sorting_array[j]
                    swapped = True

                yield True

            if not swapped:
                break

        # Sorting complete - calculate and display total time
        app_instance.complete_sorting()
        app_instance.sorted = True
        app_instance.sorting = False
        app_instance.current_indices = []
        yield False

    @staticmethod
    def use_original_bubble_sort(array):
        """
        Use the original bubble_sort from SortAlgorithm folder
        for non-visual sorting (instant sort)
        """
        return bubble_sort(array.copy())
